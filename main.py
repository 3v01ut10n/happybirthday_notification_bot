import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import database.db as db

import config


bot = telebot.TeleBot(config.token)
group_id = config.group_id
adm_id = config.adm_id


def check_admin_rights(message):
    """Проверка на админские права."""
    if str(message.from_user.id) == adm_id:
        return True


def date_convert_to_mysql_format(date):
    day, month, year = date.split(".")
    return f"{year}-{month}-{day}"


def admin_menu_keyboard():
    """Меню админки для управления ботом."""
    menu = """
Добавить именинника - /add_birthday
Отключить уведомления по имениннику - /disable_birthday
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
def add_birthday_boy(message):
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


"""# События при нажатии на кнопки меню.
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "disable_birthday_boy":
        bot.send_message(group_id, "Отключить уведомления по имениннику", parse_mode="Markdown")
    elif call.data == "send_test_group_msg":
        bot.send_message(group_id, "Тестовое сообщение")"""


if __name__ == "__main__":
    bot.polling()
