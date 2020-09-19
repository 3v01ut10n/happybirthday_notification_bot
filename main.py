import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core import *
import database.db as db
import config


bot = telebot.TeleBot(config.token)
group_id = config.group_id
adm_id = config.adm_id


def admin_menu_keyboard():
    """Меню админки для управления ботом."""
    menu = """
Добавить именинника - /add_birthday
Отключить уведомления по имениннику - /disable_birthday
Посмотреть всех именинников - /show_all_birthday
Отправить тестовое сообщение в группу - /send_test_group_msg
"""

    return menu


# Команды бота.
@bot.message_handler(commands=["admin"])
def admin_menu(message):
    """Админка для бота."""
    try:
        if check_admin_rights(message):
            bot.send_message(adm_id, admin_menu_keyboard())
    except Exception as e:
        print(e)


@bot.message_handler(commands=["add_birthday"])
def add_birthday(message):
    """Добавление именинника."""
    try:
        if check_admin_rights(message):
            bot.send_message(adm_id, 'Отправь данные в формате "Имя, дата, телефон"', parse_mode="Markdown")
            bot.register_next_step_handler(message, message_processing)
    except Exception as e:
        print(e)


def message_processing(message):
    """Обработка сообщения."""
    try:
        name, date, telephone = message.text.split(', ')
        date = date_convert_to_mysql_format(date)
        db.insert_birthday_in_db(name, date, telephone)
        bot.send_message(adm_id, "День рождения успешно добавлен")
    except ValueError:
        bot.send_message(adm_id, "Неверный формат данных. Попробуй снова - /add_birthday")


@bot.message_handler(commands=["show_all_birthday"])
def show_all_birthday(message):
    """Показать всех именинников."""
    try:
        if check_admin_rights(message):
            bot.send_message(adm_id, db.select_all_birthday_in_db())
    except Exception as e:
        print(e)


if __name__ == "__main__":
    bot.polling()
