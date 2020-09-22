from datetime import date

from database import db
from config import group_id


def put_gender(gender):
    """Подставить пол в текст."""
    if gender == "M":
        return "Ему"
    elif gender == "F":
        return "Ей"


db.connection.ping()
current_date = db.get_current_date()
active_birthdays = db.select_active_birthdays()

# Поиск именинников за сегодня.
today_birthday_boys = []
for person in active_birthdays:
    if (person["date"].day == current_date.day) and (person["date"].month == current_date.month):
        today_birthday_boys.append(person)

# Если именинник есть, проведётся отправка.
for person in today_birthday_boys:
    db.bot.send_message(
        group_id,
        f"Сегодня день рождения отмечает {person['name']}!\n"
        f"{put_gender(person['gender'])} исполняется {current_date.year - person['date'].year}.\n"
        f"Номер телефона: {person['telephone']}"
    )


# Поиск именинников за неделю.
week_birthday_boys = []
for person in active_birthdays:
    date_birthday_in_current_year = date(current_date.year, person["date"].month, person["date"].day)
    delta = (date_birthday_in_current_year - current_date).days
    if delta == 7:
        week_birthday_boys.append(person)

# Если именинник есть, проведётся отправка.
for person in week_birthday_boys:
    db.bot.send_message(
        group_id,
        f"Через неделю день рождения у {person['name']}!\n"
        f"{put_gender(person['gender'])} исполняется {current_date.year - person['date'].year}.\n"
        f"Номер телефона: {person['telephone']}"
    )
