from telebot import types
from log import log


class Forward:
    def __init__(self, develop_mode: bool):
        self.message_forward_data = dict()
        self.__develop_mode = develop_mode
        self.logger = log('forward', 'forward.log', 'INFO')

    def develop_debugging(self, method: str, info: str):
        print('Method: ', method)
        print('Global state now: ', self.message_forward_data)
        print('Info about this process: ', info)

    def add_key(self, message: types.Message):
        new_key = {
            'id': message.from_user.id,
            'username': message.from_user.username,
            'first': message.from_user.first_name,
            'last': message.from_user.last_name
        }
        self.message_forward_data[message.date] = new_key
        if self.__develop_mode:
            self.develop_debugging('add_key', f"Adding new key {message.date} => {str(new_key)}")
        self.logger.info(f"Method add_key. Information: {message.date} => {message.from_user.id}")

    def get_id(self, message):
        try:
            result: dict = self.message_forward_data.get(message.reply_to_message.date, default=KeyError)
            if self.__develop_mode:
                self.develop_debugging('get_id', f"Getting id from {str(result)}")
            self.logger.info(f"Method get_id. Information: {result}")
            return result.get('id', default=KeyError)
        except KeyError as error:
            self.logger.info(f"Error from get_key method. Information {error.with_traceback(None)}")

    def delete_data(self, message):
        try:
            result = self.message_forward_data.pop(message.reply_to_message.date, default=KeyError)
            if self.__develop_mode:
                self.develop_debugging(
                    'deleted_data',
                    f"Deleting data about a user by date: {str(message.reply_to_message.date)} => {str(result)}")
            self.logger.info(f"Method delete_data. "
                             f"Information: user id {result} was deleted by {message.reply_to_message.date}")
        except KeyError as error:
            self.logger.info(f"Error from delete_data method. Information {error.with_traceback(None)}")

    def clear_data(self):
        self.message_forward_data.clear()
        if self.__develop_mode:
            self.develop_debugging('clear_data', 'Global state is empty')
        self.logger.info(f"Method clear_data. Information: self.message_forward_data had cleared")

    def get_mode(self):
        return self.__develop_mode
