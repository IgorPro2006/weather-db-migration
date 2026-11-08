# Міграція бази даних (варіант 16)

Python + SQLAlchemy (ORM) + Alembic (міграції) + PostgreSQL / MySQL.
Датасет: [Global Weather Repository](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository).
Варіант 16 → 16 mod 4 = 0 → категорія «схід-захід небесних тіл».

## Запуск

1. `pip install -r requirements.txt`
2. Створити в pgAdmin базу `weather_db`, вказати свій пароль у `weather_app/database.py`.
3. Завантажити датасет: `python download_data.py` (сам скачає CSV з Kaggle у папку `data/`).
4. Команди:

```
alembic upgrade head
python main.py import data/GlobalWeatherRepository.csv
```
