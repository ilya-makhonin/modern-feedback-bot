import pymysql
from log import log


sql_log = log('sql', 'sql.log', 'DEBUG')


def connection():
    return pymysql.connect('connect string')


def add_user():
    pass
