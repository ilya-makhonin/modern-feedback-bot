from bot import create_bot_instance, hidden_forward
from log import log
import threading
import telebot
import flask
from time import sleep
from config import *


logger_main = log('main', './logs/main.log', 'WARNING')


def update_cache(timeout: int):
    try:
        while True:
            sleep(timeout)
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
        bot = create_bot_instance(logging_enable, logging_level)
        if use_web_hook:
            url = f"https://{HOST}:{PORT}/{TOKEN}/"
            bot.remove_webhook()
            sleep(1)
            bot.set_webhook(url=url, certificate=open(CERT, 'r'))
            server = flask_init(bot)
            server.run(host=LISTEN, port=PORT, ssl_context=(CERT, KEY))
        else:
            bot.polling(none_stop=True, interval=.5)
        timeout = 14400 if hidden_forward.get_mode() else 30
        thread = threading.Thread(target=update_cache, name='CacheThread', args=[timeout])
        thread.setDaemon(True)
        thread.start()
    except Exception as error:
        print(error)
        logger_main.warning('bot crashed')
        logger_main.warning(error.with_traceback(None))


if __name__ == '__main__':
    main(use_web_hook=True, logging_enable=True, logging_level='DEBUG')
