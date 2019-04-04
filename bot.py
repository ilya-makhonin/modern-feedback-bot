import telebot
import sql
from log import log
from constants import *
from config import TOKEN, CHAT
from forward import Forward
import logging
import json
import os


bot = telebot.TeleBot(TOKEN)
logger = log('bot', 'bot.log', 'INFO')
hidden_forward = Forward(False)


def get_user_id(user_id, message: telebot.types.Message):
    if user_id is not False:
        return user_id
    if message.reply_to_message.forward_from is None:
        return hidden_forward.get_id(message)
    return message.reply_to_message.forward_from.id


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


@bot.message_handler(commands=['helping'])
def helping_handler(message: telebot.types.Message):
    logger.info(f"User {message.from_user.id} had entered /helping command")
    admins = sql.get_admins()
    if not admins:
        bot.send_message(message.from_user.id, get_admins_error)
        logger.info(f"Error getting list of admins. User which to send /helping command: {message.from_user.id}")
        return
    if message.from_user.id in sql.get_admins():
        bot.send_message(message.from_user.id, helping_mess)
        logger.info(f"It's helping handler. Message from user {message.from_user.id}")


@bot.message_handler(commands=['usercount'])
def get_user_count(message: telebot.types.Message):
    logger.info(f"User {message.from_user.id} had entered /usercount command")
    admins = sql.get_admins()
    if not admins:
        bot.send_message(message.from_user.id, get_admins_error)
        logger.info(f"Error getting list of admins. User which to sent /usercount command: {message.from_user.id}")
        return
    if message.from_user.id in sql.get_admins():
        user_count = sql.user_count()
        if not user_count:
            bot.send_message(message.from_user.id, user_count_error)
            logger.info(f"Error getting user's count. User which to sent /usercount command: {message.from_user.id}")
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
        if text == '':
            bot.send_message(message.from_user.id, global_error)
            logger.info(f"Error global mailing. User {message.from_user.id} doesn't send a text")
            return
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


@bot.message_handler(commands=['getfullcache'])
def get_cache(message: telebot.types.Message):
    logger.info(f"User {message.from_user.id} had entered /getfullcache command")
    admins = sql.get_admins()
    if not admins:
        bot.send_message(message.from_user.id, get_admins_error)
        logger.info(f"Error getting list of admins. User which to send /getfullcache command: {message.from_user.id}")
        return
    if message.from_user.id in sql.get_admins():
        try:
            if not os.path.exists('cache/'):
                os.mkdir('./cache/')
            with open('./cache/file.txt', 'w', encoding='utf8') as cache:
                json.dump(hidden_forward.message_forward_data, cache, ensure_ascii=False, indent=2)
            doc = open('./cache/file.txt', 'rb')
            bot.send_document(message.from_user.id, doc)
            doc.close()
            logger.info(
                f"User {message.from_user.id} had gotten cache data. Result: {hidden_forward.message_forward_data}")
        except Exception as error:
            logger.info(error.with_traceback(None))


@bot.message_handler(commands=['banuser'])
def ban_user(message: telebot.types.Message):
    logger.info(f"User {message.from_user.id} had entered /banuser command")
    admins = sql.get_admins()
    if not admins:
        bot.send_message(message.from_user.id, get_admins_error)
        logger.info(f"Error getting list of admins. User which to send /banuser command: {message.from_user.id}")
        return
    if message.from_user.id in sql.get_admins():
        user_id = (message.text.split(' '))
        if len(user_id) == 0:
            user_id = False
        else:
            user_id = user_id[1].strip()
        bans = sql.ban_user(get_user_id(user_id, message))
        if not bans or len(bans) == 0:
            bot.send_message(message.from_user.id, add_ban_error)
            logger.info(f"Error at ban_user handler. User which to sent /banuser command: {message.from_user.id}")
            return
        bot.send_message(message.from_user.id, str(bans))
        logger.info(f"User {message.from_user.id} had added a user at ban. Bans list: {bans}")


@bot.message_handler(commands=['unbanuser'])
def un_ban_user(message: telebot.types.Message):
    logger.info(f"User {message.from_user.id} had entered /unbanuser command")
    admins = sql.get_admins()
    if not admins:
        bot.send_message(message.from_user.id, get_admins_error)
        logger.info(f"Error getting list of admins. User which to send /unbanuser command: {message.from_user.id}")
        return
    if message.from_user.id in sql.get_admins():
        user_id = (message.text.split(' '))
        if len(user_id) == 0:
            user_id = False
        else:
            user_id = user_id[1].strip()
        un_bans = sql.un_ban(get_user_id(user_id, message))
        if len(un_bans) == 0 and un_bans is not False:
            bot.send_message(message.from_user.id, clear_ban_mess)
            logger.info(f"Ban-list is clear. User which to sent /unbanuser command: {message.from_user.id}")
            return
        if not un_bans:
            bot.send_message(message.from_user.id, un_ban_error)
            logger.info(f"Error at un_ban_user handler. User which to sent /unbanuser command: {message.from_user.id}")
            return
        bot.send_message(message.from_user.id, str(un_bans))
        logger.info(f"User {message.from_user.id} had deleted a user from ban. Bans list: {un_bans}")


@bot.message_handler(func=lambda message: message.from_user.id in sql.get_ban_list())
def send_ban_handler(message: telebot.types.Message):
    bot.send_message(message.from_user.id, ban_mess)
    logger.info(f"It's help send_ban_handler. Message from ban-user {message.from_user.id}")


@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            if message.reply_to_message.forward_from is None:
                bot.send_sticker(hidden_forward.get_id(message), message.sticker.file_id)
            else:
                hidden_forward.delete_data(message)
                bot.send_sticker(message.reply_to_message.forward_from.id, message.sticker.file_id)
            logger.info(f"Sticker handler. In CHAT. Info: {message}")
        else:
            hidden_forward.add_key(message)
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"Sticker handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in sticker handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['photo'])
def images_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            if message.reply_to_message.forward_from is None:
                bot.send_photo(hidden_forward.get_id(message), message.photo[-1].file_id)
            else:
                hidden_forward.delete_data(message)
                bot.send_photo(message.reply_to_message.forward_from.id, message.photo[-1].file_id)
            logger.info(f"Photo handler. In CHAT. Info: {message}")
        else:
            hidden_forward.add_key(message)
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"Image handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in image handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['document'])
def file_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            if message.reply_to_message.forward_from is None:
                bot.send_document(hidden_forward.get_id(message), message.document.file_id)
            else:
                hidden_forward.delete_data(message)
                bot.send_document(message.reply_to_message.forward_from.id, message.document.file_id)
            logger.info(f"Document handler. In CHAT. Info: {message}")
        else:
            hidden_forward.add_key(message)
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"File handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in file handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['audio'])
def audio_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            if message.reply_to_message.forward_from is None:
                bot.send_audio(hidden_forward.get_id(message), message.audio.file_id)
            else:
                hidden_forward.delete_data(message)
                bot.send_audio(message.reply_to_message.forward_from.id, message.audio.file_id)
            logger.info(f"Audio handler. In CHAT. Info: {message}")
        else:
            hidden_forward.add_key(message)
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
            if message.reply_to_message.forward_from is None:
                bot.send_voice(hidden_forward.get_id(message), message.voice.file_id)
            else:
                hidden_forward.delete_data(message)
                bot.send_voice(message.reply_to_message.forward_from.id, message.voice.file_id)
            logger.info(f"Voice handler. In CHAT. Info: {message}")
        else:
            hidden_forward.add_key(message)
            bot.forward_message(CHAT, message.chat.id, message.message_id)
            bot.reply_to(message, success_mess)
            logger.info(f"Voice handler. Message from a user. Info: {message}")
    except Exception as error:
        logger.info(f"Exception in voice handler. Info: {error.with_traceback(None)}")


@bot.message_handler(content_types=['text'])
def text_handler(message: telebot.types.Message):
    try:
        if message.chat.id == int(CHAT):
            if message.reply_to_message.forward_from is None:
                bot.send_message(hidden_forward.get_id(message), message.text)
            else:
                hidden_forward.delete_data(message)
                bot.send_message(message.reply_to_message.forward_from.id, message.text)
            logger.info(f"Text handler. In CHAT. Info: {message}")
        else:
            hidden_forward.add_key(message)
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
