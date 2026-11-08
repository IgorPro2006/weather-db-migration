# Рівень запитів до БД: тільки тут звертаємося до таблиць.
from sqlalchemy import func, select

from weather_app.models import Weather


def count_weather(session):
    return session.scalar(select(func.count()).select_from(Weather))


def add_all(session, items):
    session.add_all(items)
    session.commit()
