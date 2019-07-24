from telebot import types
from config import CHAT
from helpers.sql import get_admins
import re


def create_markup(buttons, row_width=1):
    markup = types.ReplyKeyboardMarkup(True, False, row_width=row_width)
    markup.add(*buttons)
    return markup


def create_buttons_list(arr):
    if arr:
        buttons = list()
        for unit in arr:
            percent = '' if len(unit) < 3 else f"  {unit[2]}%"
            button_text = unit[1] + percent
            buttons.append(button_text)

        return create_markup(buttons)


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               "\U0001F600-\U0001F64F"
                               "\U0001F300-\U0001F5FF"
                               "\U0001F680-\U0001F6FF"  # transport & map symbols
                               "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "\U00002702-\U000027B0"
                               "\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def send_to_chat(cache, bot, message, success):
    cache.add_key(message)
    bot.forward_message(CHAT, message.chat.id, message.message_id)
    bot.send_message(CHAT, message.from_user.id)
    bot.reply_to(message, success)


def check_for_admin(message, admins):
    return message.from_user.id in admins
