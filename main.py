import telebot

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
Включить уведомления по имениннику - /enable_birthday

Посмотреть всех именинников - /show_all_birthdays
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
        bot.send_message(adm_id, f"При выполнении check_admin_rights возникла ошибка: {e}")


@bot.message_handler(commands=["add_birthday"])
def add_birthday(message):
    """Добавление именинника."""
    try:
        if check_admin_rights(message):
            bot.send_message(
                adm_id,
                f'Отправь данные в формате "Имя, дата, телефон, пол".\n'
                f'Пример - "Иван Иванов, 01.01.1990, 89991234567, M"',
                parse_mode="Markdown")
            bot.register_next_step_handler(message, add_message_processing)
    except Exception as e:
        bot.send_message(adm_id, f"При выполнении add_birthday возникла ошибка: {e}")


def add_message_processing(message):
    """Обработка сообщения с информацией о добавлении."""
    try:
        name, date, telephone, gender = message.text.split(', ')
        date = date_convert_to_mysql_format(date)
        db.insert_birthday(name, date, telephone, gender)
        bot.send_message(adm_id, "День рождения успешно добавлен")
    except ValueError:
        bot.send_message(adm_id, "Неверный формат данных. Попробуй снова - /add_birthday")


@bot.message_handler(commands=["disable_birthday"])
def disable_birthday(message):
    """Отключить уведомления по имениннику."""
    try:
        if check_admin_rights(message):
            birthdays = db.select_birthday(active=True)
            if birthdays:
                bot.send_message(adm_id, f"Для какого человека отключить уведомления? Введи ID.\n{birthdays}")
                bot.register_next_step_handler(message, disable_message_processing)
            else:
                bot.send_message(adm_id, "Сейчас уведомления отключены для всех")
    except Exception as e:
        bot.send_message(adm_id, f"При выполнении disable_birthday возникла ошибка: {e}")


def disable_message_processing(message):
    """Обработка сообщения с информацией об отключении."""
    try:
        id = message.text
        db.manage_notify_birthday(id, mode="disable")
        bot.send_message(adm_id, "Уведомления для этого человека отключены")
    except ValueError:
        bot.send_message(adm_id, "Неверный формат данных. Попробуй снова - /disable_birthday")


@bot.message_handler(commands=["enable_birthday"])
def enable_birthday(message):
    """Включить уведомления по имениннику."""
    try:
        if check_admin_rights(message):
            birthdays = db.select_birthday(active=False)
            if birthdays:
                bot.send_message(adm_id, f"Для какого человека включить уведомления? Введи ID.\n{birthdays}")
                bot.register_next_step_handler(message, enable_message_processing)
            else:
                bot.send_message(adm_id, "Сейчас уведомления включены для всех")
    except Exception as e:
        bot.send_message(adm_id, f"При выполнении enable_birthday возникла ошибка: {e}")


def enable_message_processing(message):
    """Обработка сообщения с информацией о включении."""
    try:
        id = message.text
        db.manage_notify_birthday(id, mode="enable")
        bot.send_message(adm_id, "Уведомления для этого человека включены")
    except ValueError:
        bot.send_message(adm_id, "Неверный формат данных. Попробуй снова - /enable_birthday")


@bot.message_handler(commands=["show_all_birthdays"])
def show_all_birthdays(message):
    """Показать всех именинников."""
    try:
        if check_admin_rights(message):
            bot.send_message(adm_id, db.select_all_birthdays())
    except Exception as e:
        bot.send_message(adm_id, f"При выполнении show_all_birthdays возникла ошибка: {e}")


if __name__ == "__main__":
    bot.polling()
