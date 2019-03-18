import telebot
import sql
from log import log
from constants import *
from config import TOKEN, CHAT
import logging


bot = telebot.TeleBot(TOKEN)
logger = log('bot', 'bot.log', 'INFO')


@bot.message_handler(commands=['start'])
def start_handler(message: telebot.types.Message):
    adding = sql.add_user(
        message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    if not adding:
        sql.sql_log.error(f"Error in start handler! User {message.from_user.id} did not have added to the bot")
        return
    bot.send_message(message.from_user.id, start_mess)
    logger.info(f"It's start handler. User {message.from_user.id} had added to the bot")


@bot.message_handler(commands=['help'])
def help_handler(message: telebot.types.Message):
    bot.send_message(message.from_user.id, help_mess)
    logger.info(f"It's help handler. Message from user {message.from_user.id}")


@bot.message_handler(commands=['user_count'])
def get_user_count(message: telebot.types.Message):
    logger.info(f"User {message.from_user.id} had entered /user_count command")
    admins = sql.get_admins()
    if not admins:
        bot.send_message(message.from_user.id, get_admins_error)
        logger.info(f"Error getting list of admins. User which to send /user_count command: {message.from_user.id}")
        return
    if message.from_user.id in sql.get_admins():
        user_count = sql.user_count()
        if not user_count:
            bot.send_message(message.from_user.id, user_count_error)
            logger.info(f"Error getting user's count. User which to send /user_count command: {message.from_user.id}")
            return
        bot.send_message(message.from_user.id, count_mess.format(user_count))
        logger.info(f"User {message.from_user.id} had gotten user's count. Result: {user_count}")


@bot.message_handler(commands=['global'])
def global_mailing(message: telebot.types.Message):
    logger.info(f"User {message.from_user.id} had entered /global command")
    admins = sql.get_admins()
    if not admins:
        bot.send_message(message.from_user.id, get_admins_error)
        logger.info(f"Error getting list of admins. User which to send /global command: {message.from_user.id}")
        return
    if message.from_user.id in sql.get_admins():
        text = (message.text[7:]).strip()
        deleted_user = 0
        users = sql.get_users()
        if not users:
            bot.send_message(message.from_user.id, get_user_error)
            logger.info(f"Error getting list of users. User which to send /global command: {message.from_user.id}")
            return
        for user in users:
            try:
                bot.send_message(user, text)
                logger.info(f"User {user} is using the bot. A message had sent successfully")
            except Exception as error:
                deleted_user += 1
                logger.info(f"User {user} is'nt using the bot. "
                            f"Error in global mailing function: {error.with_traceback(None)}")
        bot.send_message(message.from_user.id, deleted_mess.format(deleted_user))
        logger.info(f"User {message.from_user.id} had sent global mailing. Text: {text}. Deleted user: {deleted_user}")


@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            bot.send_sticker(message.reply_to_message.forward_from.id, message.sticker.file_id)
            logger.info(f"Sticker handler. In CHAT. Info: {message}")
        else:
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"Sticker handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in sticker handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['photo'])
def images_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            bot.send_photo(message.reply_to_message.forward_from.id, message.photo[-1].file_id)
            logger.info(f"Photo handler. In CHAT. Info: {message}")
        else:
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"Image handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in image handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['document'])
def file_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            bot.send_document(message.reply_to_message.forward_from.id, message.document.file_id)
            logger.info(f"Document handler. In CHAT. Info: {message}")
        else:
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"File handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in file handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['audio'])
def audio_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            bot.send_audio(message.reply_to_message.forward_from.id, message.audio.file_id)
            logger.info(f"Audio handler. In CHAT. Info: {message}")
        else:
            bot.send_audio(CHAT, message.audio.file_id,
                           caption=info_mess.format(message.from_user.first_name, message.from_user.username),
                           reply_to_message_id=message.from_user.id)
            bot.send_message(message.from_user.id, other_mess)
            logger.info(f"Audio handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in audio handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['voice'])
def voice_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            bot.send_voice(message.reply_to_message.forward_from.id, message.voice.file_id)
            logger.info(f"Voice handler. In CHAT. Info: {message}")
        else:
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"Voice handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in voice handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['text'])
def text_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            bot.send_message(message.reply_to_message.forward_from.id, message.text)
            logger.info(f"Text handler. In CHAT. Info: {message}")
        else:
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"Text handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in text handler. Info: {error.with_traceback(None)}")


@bot.message_handler(func=lambda message: True)
def other_handler(message: telebot.types.Message):
    bot.send_message(message.from_user.id, other_mess)
    logger.info(f"Other handler. Message from a user. Info: {message}")


def create_bot_instance(logging_enable=True, logging_level='DEBUG'):
    if logging_enable:
        telebot.logger.setLevel(logging.getLevelName(logging_level))
    return bot
