# Міграція бази даних (варіант 16)

Python + SQLAlchemy (ORM) + Alembic (міграції) + PostgreSQL / MySQL.
Датасет: [Global Weather Repository](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository).
Варіант 16 → 16 mod 4 = 0 → категорія «схід-захід небесних тіл».

| Гілка | Етап |
|---|---|
| `stage-1` | ORM-модель, таблиця `weather`, імпорт CSV |
| `stage-2` | дані про схід-захід винесено в таблицю `astronomy` |
| `stage-3` | колонка `go_outside` — «Чи варто виходити на вулицю» (так, якщо надворі день) |
| `stage-4` | пошук за країною і датою |
| `stage-5` / `main` | перенесення на MySQL |

## Запуск

1. `pip install -r requirements.txt`
2. Створити базу `weather_db` у pgAdmin (і в MySQL для етапу 5), вказати свої паролі
   у `weather_app/database.py`.
3. Завантажити датасет: `python download_data.py` (сам скачає CSV з Kaggle у папку `data/`).
4. Команди:

```
alembic upgrade head
python main.py import data/GlobalWeatherRepository.csv
python main.py search Ukraine 2024-05-16
python main.py search Ukraine 2024-05-16 Kyiv

alembic -x db=mysql upgrade head
python main.py copy
```
