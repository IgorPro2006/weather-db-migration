# Рівень бізнес-логіки.
from sqlalchemy.orm import Session

from weather_app import repository
from weather_app.csv_reader import read_rows
from weather_app.database import get_engine
from weather_app.models import Astronomy, Weather


def should_go_outside(last_updated, sunrise, sunset):
    """Чи варто виходити на вулицю: так, якщо надворі день (Сонце над горизонтом)."""
    if sunrise is None or sunset is None:
        return False
    now = last_updated.time()
    if sunrise < sunset:
        return sunrise <= now < sunset
    return now >= sunrise or now < sunset   # захід після півночі


def import_csv(path, db="postgres"):
    with Session(get_engine(db)) as session:
        if repository.count_weather(session) > 0:
            print("Дані вже імпортовано - таблиця weather не порожня.")
            return
        batch = []
        total = 0
        for row in read_rows(path):
            astronomy = Astronomy(
                sunrise=row.pop("sunrise"),
                sunset=row.pop("sunset"),
                moonrise=row.pop("moonrise"),
                moonset=row.pop("moonset"),
                moon_phase=row.pop("moon_phase"),
                moon_illumination=row.pop("moon_illumination"),
            )
            astronomy.go_outside = should_go_outside(
                row["last_updated"], astronomy.sunrise, astronomy.sunset)
            batch.append(Weather(**row, astronomy=astronomy))
            if len(batch) == 5000:          # зберігаємо частинами, щоб не забивати пам'ять
                repository.add_all(session, batch)
                total += len(batch)
                batch = []
        repository.add_all(session, batch)
        total += len(batch)
    print(f"Імпортовано записів: {total}")


def search(country, day, city=None, db="postgres"):
    with Session(get_engine(db)) as session:
        records = repository.find_weather(session, country, day, city)
        if not records:
            print("Нічого не знайдено.")
        for weather in records:
            print("=" * 40)
            for column in Weather.__table__.columns:
                print(f"{column.name:20} {getattr(weather, column.name)}")
            for column in Astronomy.__table__.columns:
                if column.name not in ("id", "weather_id"):
                    print(f"{column.name:20} {getattr(weather.astronomy, column.name)}")


def copy_to_mysql():
    """Копіює всі дані з Postgres у MySQL (схему в MySQL створюють ті самі міграції)."""
    tables = [Weather.__table__, Astronomy.__table__]
    with Session(get_engine("postgres")) as source, Session(get_engine("mysql")) as target:
        if repository.count_weather(target) > 0:
            print("У MySQL вже є дані.")
            return
        for table in tables:
            rows = repository.get_rows(source, table)
            repository.insert_rows(target, table, rows)
            print(f"{table.name}: скопійовано {len(rows)} рядків")
        target.commit()

        same = all(repository.get_rows(source, t) == repository.get_rows(target, t) for t in tables)
        print("Бази однакові." if same else "Бази відрізняються!")
