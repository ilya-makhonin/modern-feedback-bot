from bot import create_bot_instance
from log import log
import telebot
import flask
from config import *


logger_main = log('main', './logs/main.log', 'WARNING')


def flask_init(bot_object):
    web_hook_app = flask.Flask(__name__)
    url_path = "/%s/" % (TOKEN,)

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


def start(use_webhook=False, **webhook_data):
    try:
        bot_object = create_bot_instance(webhook_data=webhook_data, use_webhook=use_webhook, logging_enable=True)
        if use_webhook:
            server = flask_init(bot_object)
            server.run(host=LISTEN, port=PORT, ssl_context=(CERT, KEY))
            return True
        return False
    except Exception as err:
        logger_main.warning('bot crashed')
        logger_main.warning(err.with_traceback(None))


if __name__ == '__main__':
    try:
        app = start(use_webhook=True, webhook_ip=HOST, webhook_port=PORT, token=TOKEN, ssl_cert=CERT)
    except Exception as error:
        logger_main.warning(error.with_traceback(None))
        print(error)
