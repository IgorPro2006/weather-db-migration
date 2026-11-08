# Рівень запитів до БД: тільки тут звертаємося до таблиць.
from sqlalchemy import Date, cast, func, select

from weather_app.models import Weather


def count_weather(session):
    return session.scalar(select(func.count()).select_from(Weather))


def add_all(session, items):
    session.add_all(items)
    session.commit()


def find_weather(session, country, day, city=None):
    query = (select(Weather)
             .where(func.lower(Weather.country) == country.lower())
             .where(cast(Weather.last_updated, Date) == day))
    if city:
        query = query.where(func.lower(Weather.location_name) == city.lower())
    return session.scalars(query.order_by(Weather.location_name)).all()
