from telebot import types
from log import log


class Forward:
    def __init__(self):
        self.message_forward_data = dict()
        self.logger = log('forward', 'forward.log', 'INFO')

    def add_key(self, message: types.Message):
        self.message_forward_data[message.date] = message.from_user.id
        self.logger.info(f"Method add_key. Information: {message.date} => {message.from_user.id}")

    def get_id(self, message):
        try:
            result = self.message_forward_data.get(message.reply_to_message.date, default=KeyError)
            self.logger.info(f"Method get_id. Information: {result}")
            return result
        except KeyError as error:
            self.logger.info(f"Error from get_key method. Information {error.with_traceback(None)}")
            pass

    def delete_data(self, message):
        try:
            result = self.message_forward_data.pop(message.reply_to_message.date, default=KeyError)
            self.logger.info(f"Method delete_data. "
                             f"Information: user id {result} was deleted by {message.reply_to_message.date}")
        except KeyError as error:
            self.logger.info(f"Error from delete_data method. Information {error.with_traceback(None)}")
            pass

    def clear_data(self):
        self.message_forward_data.clear()
        self.logger.info(f"Method clear_data. Information: self.message_forward_data had cleared")
