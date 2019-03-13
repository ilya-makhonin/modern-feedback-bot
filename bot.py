import telebot
import constants
import sql
from log import log
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def create_bot_instance():
    return bot
