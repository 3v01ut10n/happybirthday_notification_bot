import pymysql.cursors

import config
from main import bot, adm_id
from core import date_convert_from_mysql_format


# Подключение к базе.
connection = pymysql.connect(
    **config.db,
    cursorclass=pymysql.cursors.DictCursor
)


def insert_birthday(name, date, telephone):
    """Добавить день рождения в базу."""
    connection.ping()
    try:
        cursor = connection.cursor()
        sql = f"INSERT INTO `happy_birthdays` (id, name, date, telephone, active) " \
              f"VALUES (DEFAULT, '{name}', '{date}', '{telephone}', '1');"
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
        bot.send_message(adm_id, "При добавлении произошла ошибка")


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
        print(e)
        bot.send_message(adm_id, "При получении списка возникла ошибка")


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
            print(e)
            bot.send_message(adm_id, "При получении списка возникла ошибка")
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
            print(e)
            bot.send_message(adm_id, "При получении списка возникла ошибка")


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
        bot.send_message(adm_id, "При получении списка возникла ошибка")


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
            print(e)
            bot.send_message(adm_id, "При отключении возникла ошибка")
    elif mode == "enable":
        try:
            cursor = connection.cursor()
            sql = f"UPDATE `happy_birthdays` SET active = '1' WHERE id = '{id}';"
            cursor.execute(sql)
        except Exception as e:
            print(e)
            bot.send_message(adm_id, "При включении возникла ошибка")


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
        bot.send_message(adm_id, "При получении системной даты возникла ошибка")
