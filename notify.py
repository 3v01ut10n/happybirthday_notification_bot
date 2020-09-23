from datetime import date

from database import db
from config import group_id


def put_gender(gender):
    """Подставить пол в уведомление."""
    if gender == "M":
        return "Ему"
    elif gender == "F":
        return "Ей"


def put_ending_for_age(age):
    """Подставить окончание для возраста в уведомление."""
    if age == 1 or (age >= 21 and age % 10 == 1):
        return "год"
    elif 5 <= age <= 20:
        return "лет"
    elif (age % 10 == 2) or (age % 10 == 3) or (age % 10 == 4):
        return "года"
    elif (age % 10 == 5) or (age % 10 == 6) or (age % 10 == 7) or (age % 10 == 8) or (age % 10 == 9) or (age % 10 == 0):
        return "лет"


def get_message(when_birthday, name, gender, age, ending_for_age, telephone):
    """Формирование сообщения для уведомления."""
    return f"{when_birthday} день рождения отмечает {name}!\n"\
           f"{gender} исполняется {age} {ending_for_age}.\n"\
           f"Номер телефона: {telephone}"


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
    current_age = current_date.year - person['date'].year
    db.bot.send_message(
        group_id,
        get_message(
            when_birthday="Сегодня",
            name=person['name'],
            gender=put_gender(person['gender']),
            age=current_age,
            ending_for_age=put_ending_for_age(current_age),
            telephone=person['telephone']
        )
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
    current_age = current_date.year - person['date'].year
    db.bot.send_message(
        group_id,
        get_message(
            when_birthday="Через неделю",
            name=person['name'],
            gender=put_gender(person['gender']),
            age=current_age,
            ending_for_age=put_ending_for_age(current_age),
            telephone=person['telephone']
        )
    )
