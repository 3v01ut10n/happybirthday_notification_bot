import pymysql.cursors

from main import bot, adm_id

# Подключение к базе.
connection = pymysql.connect(
    host='151.248.122.230',
    user='ekoadmin_happyb',
    password='mOdG$FeWSb^sNHsm',
    db='ekoadmin_happybot',
    cursorclass=pymysql.cursors.DictCursor
)


def insert_birthday_in_db(name, date, telephone):
    try:
        cursor = connection.cursor()
        sql = f"INSERT INTO `happy_birthdays` (id, name, date, telephone) " \
              f"VALUES (DEFAULT, '{name}', '{date}', '{telephone}');"
        cursor.execute(sql)
        connection.commit()
    except:
        bot.send_message(adm_id, "При добавлении произошла ошибка.")

    finally:
        connection.close()
