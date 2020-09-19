import datetime

from database import db
from config import group_id


server_time = datetime.datetime.now().strftime("%m-%d")
db.check_connection()
active_birthdays = db.select_active_birthdays()

# Поиск именинников.
birthday_boys = []
for person in active_birthdays:
    if person["date"].strftime("%m-%d") == server_time:
        birthday_boys.append(person)

# Если именинник есть, проведётся отправка.
for person in birthday_boys:
    db.bot.send_message(
        group_id,
        f"Сегодня день рождения отмечает {person['name']}!\n"
        f"Ему исполняется {datetime.datetime.now().year-int(person['date'].strftime('%Y'))}.\n"
        f"Номер телефона: {person['telephone']}"
    )
