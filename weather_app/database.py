# Рівень доступу до БД: логіни, паролі й підключення.
# Впишіть свої логіни й паролі (будь-які символи в паролі, наприклад @ # : /, допустимі).
from sqlalchemy import URL, create_engine

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

DATABASES = {
    "postgres": URL.create(
        "postgresql+psycopg2",
        username=POSTGRES_USER, password=POSTGRES_PASSWORD,
        host="localhost", port=5432, database="weather_db",
    ),
    "mysql": URL.create(
        "mysql+pymysql",
        username=MYSQL_USER, password=MYSQL_PASSWORD,
        host="localhost", port=3306, database="weather_db",
        query={"charset": "utf8mb4"},
    ),
}


def get_engine(db="postgres"):
    return create_engine(DATABASES[db])
