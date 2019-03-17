import pymysql
from log import log
from config import HOSTD, USER, PASS, DB


sql_log = log('sql', 'sql.log', 'ERROR')


def get_connection():
    return pymysql.connections.Connection(host=HOSTD, user=USER, password=PASS, db=DB, charset='utf8mb4')


def add_user(user_id, first_name, last_name, username):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE user_id = %s;', (user_id,))
            if cursor.fetchone() is None:
                if username is not None and len(username) > 35:
                    username = username[0:35]
                if first_name is not None and len(first_name) > 100:
                    first_name = first_name[0:100]
                if last_name is not None and len(last_name) > 100:
                    last_name = last_name[0:100]
                cursor.execute(
                    'INSERT INTO `users` (user_id, username, first_name, last_name) VALUES (%s, %s, %s, %s);',
                    (user_id, username, first_name, last_name))
            connection.commit()
            return True
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


def user_count():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(id) FROM users;')
            return cursor.fetchone()[0]
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


def get_users():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT username FROM users;')
            users = cursor.fetchall()
            return [user[0] for user in users]
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()


def get_admins():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT admin_id FROM admins;')
            admins_id = cursor.fetchall()
            return [admin_id[0] for admin_id in admins_id]
    except Exception as error:
        sql_log.error(error.with_traceback(None))
        return False
    finally:
        connection.close()
