from database import db
from config import group_id


db.connection.ping()
current_date = db.get_current_date()
active_birthdays = db.select_active_birthdays()

# Поиск именинников за сегодня.
birthday_boys = []
for person in active_birthdays:
    if (person["date"].day == current_date.day) and (person["date"].month == current_date.month):
        birthday_boys.append(person)

# Если именинник есть, проведётся отправка.
for person in birthday_boys:
    db.bot.send_message(
        group_id,
        f"Сегодня день рождения отмечает {person['name']}!\n"
        f"Ему исполняется {current_date.year - person['date'].year}.\n"
        f"Номер телефона: {person['telephone']}"
    )
