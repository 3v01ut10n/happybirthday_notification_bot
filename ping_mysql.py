from database import db


db.ping_connection()
db.select_birthday(active=False)
db.bot.send_message(db.adm_id, "Cron работает")
