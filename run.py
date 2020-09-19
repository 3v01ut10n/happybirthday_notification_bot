import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import config


bot = telebot.TeleBot(config.token)
group_id = config.group_id
adm_id = config.adm_id


def admin_menu_keyboard():
    """Админка для управления ботом."""
    main_menu = InlineKeyboardMarkup(row_width=1)  # 1 = каждая команда на новой линии.
    main_menu.add(InlineKeyboardButton("Добавить именинника", callback_data="add_birthday_boy"),
                  InlineKeyboardButton("Отключить уведомления по имениннику", callback_data="disable_birthday_boy"),
                  InlineKeyboardButton("Отправить тестовое сообщение в группу", callback_data="send_test_group_msg")
                  )

    return main_menu


# Команды бота.
@bot.message_handler(commands=["admin"])
def admin_menu(message):
    """Админка для бота."""
    try:
        if str(message.from_user.id) == adm_id:
            bot.send_message(message.from_user.id, "Что будем делать?", reply_markup=admin_menu_keyboard())
    except:
        pass


# События при нажатии на кнопки меню.
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "add_birthday_boy":
        bot.send_message(group_id, "Добавить именинника", parse_mode="Markdown")
    elif call.data == "disable_birthday_boy":
        bot.send_message(group_id, "Отключить уведомления по имениннику", parse_mode="Markdown")
    elif call.data == "send_test_group_msg":
        bot.send_message(group_id, "Тестовое сообщение")


if __name__ == "__main__":
    bot.polling()
