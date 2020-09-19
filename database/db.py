import pymysql.cursors

from main import bot, adm_id
from core import date_convert_from_mysql_format
import config


# Подключение к базе.
connection = pymysql.connect(
    **config.db,
    cursorclass=pymysql.cursors.DictCursor
)


def insert_birthday(name, date, telephone):
    """Добавить день рождения в базу."""
    try:
        cursor = connection.cursor()
        sql = f"INSERT INTO `happy_birthdays` (id, name, date, telephone, active) " \
              f"VALUES (DEFAULT, '{name}', '{date}', '{telephone}', '1');"
        cursor.execute(sql)
        connection.commit()
    except:
        bot.send_message(adm_id, "При добавлении произошла ошибка")


def select_all_birthday():
    """Получить все дни рождения из базы."""
    try:
        data = ""
        cursor = connection.cursor()
        sql = f"SELECT * FROM `happy_birthdays`"
        cursor.execute(sql)
        birthdays = cursor.fetchall()
        for birthday in birthdays:
            data += f"{birthday['name']} - {date_convert_from_mysql_format(birthday['date'])}\n"
        return data
    except:
        bot.send_message(adm_id, "При получении списка возникла ошибка")


def select_active_birthday():
    """Получить все активные дни рождения из базы."""
    try:
        data = ""
        cursor = connection.cursor()
        sql = f"SELECT * FROM `happy_birthdays` WHERE active = '1';"
        cursor.execute(sql)
        birthdays = cursor.fetchall()
        for birthday in birthdays:
            data += f"{birthday['id']}. {birthday['name']} - {date_convert_from_mysql_format(birthday['date'])}\n"
        return data
    except:
        bot.send_message(adm_id, "При получении списка возникла ошибка")


def disable_birthday(id):
    """Отключить уведомления по дню рождения для выбранного человека."""
    try:
        cursor = connection.cursor()
        sql = f"UPDATE `happy_birthdays` SET active = '0' WHERE id = '{id}';"
        cursor.execute(sql)
    except:
        bot.send_message(adm_id, "При отключении возникла ошибка")
