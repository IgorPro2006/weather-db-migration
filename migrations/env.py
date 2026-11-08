# Alembic запускає цей файл перед кожною міграцією.
# Вибір бази: alembic upgrade head              (Postgres)
#             alembic -x db=mysql upgrade head  (MySQL)
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from weather_app.database import DATABASES

fileConfig(context.config.config_file_name, disable_existing_loggers=False)
db = context.get_x_argument(as_dictionary=True).get("db", "postgres")
engine = create_engine(DATABASES[db])

with engine.connect() as connection:
    context.configure(connection=connection)
    with context.begin_transaction():
        context.run_migrations()
