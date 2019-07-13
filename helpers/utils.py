from telebot import types


def create_markup(buttons, row_width=1):
    """
    Создает клавиатуру с кнопками из списка buttons и шириной строк row
    :param buttons: <list> like [['button_text', 'callback_data'], ...]
    :param row_width: <int> number of buttons per line
    :return: <class 'telebot.types.InlineKeyboardMarkup'>
    """
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
