import config


def check_admin_rights(message):
    """Проверка на админские права."""
    if str(message.from_user.id) == config.adm_id:
        return True


def date_convert_to_mysql_format(date):
    """Конвертация даты в формат MySQL."""
    day, month, year = date.split(".")
    return f"{year}-{month}-{day}"


def date_convert_from_mysql_format(date):
    """Конвертация даты из формата MySQL."""
    return date.strftime("%d.%m.%Y")
