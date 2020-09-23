import pymysql.cursors

import config
from main import bot, adm_id
from core import date_convert_from_mysql_format


# Подключение к базе.
connection = pymysql.connect(
    **config.db,
    cursorclass=pymysql.cursors.DictCursor
)


def insert_birthday(name, date, telephone, gender):
    """Добавить день рождения в базу."""
    connection.ping()
    try:
        cursor = connection.cursor()
        sql = f"INSERT INTO `happy_birthdays` (id, name, date, telephone, gender, active) " \
              f"VALUES (DEFAULT, '{name}', '{date}', '{telephone}', '{gender}', '1');"
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        bot.send_message(adm_id, f"При выполнении insert_birthday произошла ошибка: {e}")


def select_all_birthdays():
    """Получить все дни рождения из базы."""
    connection.ping()
    try:
        data = ""
        cursor = connection.cursor()
        sql = f"SELECT * FROM `happy_birthdays`"
        cursor.execute(sql)
        birthdays = cursor.fetchall()
        for birthday in birthdays:
            data += f"{birthday['name']} - {date_convert_from_mysql_format(birthday['date'])}\n"
        return data
    except Exception as e:
        bot.send_message(adm_id, f"При выполнении select_all_birthdays возникла ошибка: {e}")


def select_birthday(active):
    """
    Получить все активные/неактивные дни рождения из базы.
    active = True/False
    """
    connection.ping()
    if active:
        try:
            data = ""
            cursor = connection.cursor()
            sql = f"SELECT * FROM `happy_birthdays` WHERE active = '1';"
            cursor.execute(sql)
            birthdays = cursor.fetchall()
            for birthday in birthdays:
                data += f"{birthday['id']}. {birthday['name']} - {date_convert_from_mysql_format(birthday['date'])}\n"
            return data
        except Exception as e:
            bot.send_message(adm_id, f"При выполнении select_birthday(if active) возникла ошибка: {e}")
    else:
        try:
            data = ""
            cursor = connection.cursor()
            sql = f"SELECT * FROM `happy_birthdays` WHERE active = '0';"
            cursor.execute(sql)
            birthdays = cursor.fetchall()
            for birthday in birthdays:
                data += f"{birthday['id']}. {birthday['name']} - {date_convert_from_mysql_format(birthday['date'])}\n"
            return data
        except Exception as e:
            bot.send_message(adm_id, f"При выполнении select_birthday(else) возникла ошибка: {e}")


def select_active_birthdays():
    """Активные дни рождения в сыром виде из базы."""
    connection.ping()
    try:
        cursor = connection.cursor()
        sql = f"SELECT * FROM `happy_birthdays` WHERE active = '1';"
        cursor.execute(sql)
        birthdays = cursor.fetchall()
        return birthdays
    except Exception as e:
        print(e)
        bot.send_message(adm_id, f"При выполнении select_active_birthdays возникла ошибка: {e}")


def manage_notify_birthday(id, mode):
    """
    Отключить/включить уведомления по дню рождения для выбранного человека.
    mode = disable/enable
    """
    connection.ping()
    if mode == "disable":
        try:
            cursor = connection.cursor()
            sql = f"UPDATE `happy_birthdays` SET active = '0' WHERE id = '{id}';"
            cursor.execute(sql)
        except Exception as e:
            bot.send_message(adm_id, f"При выполнении manage_notify_birthday(disable) возникла ошибка: {e}")
    elif mode == "enable":
        try:
            cursor = connection.cursor()
            sql = f"UPDATE `happy_birthdays` SET active = '1' WHERE id = '{id}';"
            cursor.execute(sql)
        except Exception as e:
            print(e)
            bot.send_message(adm_id, f"При выполнении manage_notify_birthday(enable) возникла ошибка: {e}")


def get_current_date():
    """Получить текущую дату из базы данных."""
    connection.ping()
    try:
        cursor = connection.cursor()
        sql = f"SELECT CURRENT_DATE FROM `happy_birthdays`;"
        cursor.execute(sql)
        return cursor.fetchone()["CURRENT_DATE"]
    except Exception as e:
        print(e)
        bot.send_message(adm_id, f"При выполнении get_current_date возникла ошибка: {e}")
