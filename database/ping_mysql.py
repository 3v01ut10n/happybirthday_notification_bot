from database import db


db.ping_connection()
db.select_birthday(active=False)
