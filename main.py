from bot import create_bot_instance, hidden_forward, bot_cache
from helpers.log import log
import threading
import telebot
import flask
from time import sleep
from config import *


logger_main = log('main', 'main.log', 'WARNING')


def update_cache(timeout: int):
    try:
        while True:
            sleep(timeout)
            bot_cache.update_cache()
            hidden_forward.clear_data()
    except Exception as err:
        logger_main.warning(err.with_traceback(None))


def flask_init(bot_object):
    web_hook_app = flask.Flask(__name__)
    url_path = f"/{TOKEN}/"

    @web_hook_app.route('/', methods=['GET', 'HEAD'])
    def index():
        return ''

    @web_hook_app.route(url_path, methods=['POST'])
    def webhook():
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot_object.process_new_updates([update])
            return ''
        else:
            logger_main.warning('Abort 403')
            flask.abort(403)
    return web_hook_app


def main(use_web_hook, logging_enable, logging_level):
    try:
        _bot = create_bot_instance(logging_enable, logging_level)
        # TODO: Как вариант, убрать многопоточность, так как весь кэш будет обновляться автоматически
        timeout = 120 if hidden_forward.get_mode() else (60 * 60 * 24)
        thread = threading.Thread(target=update_cache, name='CacheThread', args=[timeout])
        thread.setDaemon(True)
        thread.start()
        if use_web_hook:
            url = f"https://{HOST}:{PORT}/{TOKEN}/"
            _bot.remove_webhook()
            sleep(1)
            _bot.set_webhook(url=url, certificate=open(CERT, 'r'))
            server = flask_init(_bot)
            server.run(host=LISTEN, port=PORT, ssl_context=(CERT, KEY))
        else:
            _bot.polling(none_stop=True, interval=.5)
    except Exception as error:
        print(error)
        logger_main.warning('bot crashed')
        logger_main.warning(error.with_traceback(None))


if __name__ == '__main__':
    main(use_web_hook=True, logging_enable=True, logging_level='INFO')
