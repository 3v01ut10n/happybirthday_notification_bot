# Happy Birthday Notification Bot
Telegram-бот, который напомнит, когда у вашего друга день рождения.  
Написан на Python 3.8.

## Описание файлов
```
├── database
│   └── db.py  # Запросы к базе данных.
│
│── config-sample.py  # Пример конфига.
│── core.py  # Функции, необходимые для работы.
│── main.py  # Запуск бота.
│── notify.py  # Ежедневная проверка и отправка уведомления.
│── requirements.txt  # Зависимости для работы бота.
```

### Установка
* Устанавливаем пакеты pip:
```
pip install -r requirements.txt
```
* Переименовываем **config-sample.py** в **config.py** и настраиваем под себя.
* Импортируем dump.sql в базу данных.
* Добавляем cron-задание на ежедневное уведомление по примеру:
```
0 8 * * * /usr/local/bin/python3.8 /home/admin/happybirthday_notification_bot/notify.py
```
* Создаём группу в Telegram, добавляем бота и людей, которым эти уведомления также необходимы.