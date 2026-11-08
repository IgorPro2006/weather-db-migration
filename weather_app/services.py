# Рівень бізнес-логіки.
from sqlalchemy.orm import Session

from weather_app import repository
from weather_app.csv_reader import read_rows
from weather_app.database import get_engine
from weather_app.models import Weather


def import_csv(path, db="postgres"):
    with Session(get_engine(db)) as session:
        if repository.count_weather(session) > 0:
            print("Дані вже імпортовано - таблиця weather не порожня.")
            return
        batch = []
        total = 0
        for row in read_rows(path):
            batch.append(Weather(**row))
            if len(batch) == 5000:          # зберігаємо частинами, щоб не забивати пам'ять
                repository.add_all(session, batch)
                total += len(batch)
                batch = []
        repository.add_all(session, batch)
        total += len(batch)
    print(f"Імпортовано записів: {total}")
