from telebot import types
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
