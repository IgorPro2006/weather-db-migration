"""Етап 2: перенесення даних про схід-захід у таблицю astronomy"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"

COLUMNS = ["sunrise", "sunset", "moonrise", "moonset", "moon_phase", "moon_illumination"]


def upgrade():
    # 1. нова таблиця
    op.create_table(
        "astronomy",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("weather_id", sa.Integer, sa.ForeignKey("weather.id"), nullable=False, unique=True),
        sa.Column("sunrise", sa.Time),
        sa.Column("sunset", sa.Time),
        sa.Column("moonrise", sa.Time),
        sa.Column("moonset", sa.Time),
        sa.Column("moon_phase", sa.String(20)),
        sa.Column("moon_illumination", sa.Integer),
    )
    # 2. копіюємо дані
    op.execute("""
        INSERT INTO astronomy (weather_id, sunrise, sunset, moonrise, moonset, moon_phase, moon_illumination)
        SELECT id, sunrise, sunset, moonrise, moonset, moon_phase, moon_illumination FROM weather
    """)
    # 3. лише тепер видаляємо старі колонки
    for column in COLUMNS:
        op.drop_column("weather", column)


def downgrade():
    op.add_column("weather", sa.Column("sunrise", sa.Time))
    op.add_column("weather", sa.Column("sunset", sa.Time))
    op.add_column("weather", sa.Column("moonrise", sa.Time))
    op.add_column("weather", sa.Column("moonset", sa.Time))
    op.add_column("weather", sa.Column("moon_phase", sa.String(20)))
    op.add_column("weather", sa.Column("moon_illumination", sa.Integer))
    for column in COLUMNS:
        op.execute(f"UPDATE weather SET {column} = "
                   f"(SELECT a.{column} FROM astronomy a WHERE a.weather_id = weather.id)")
    op.drop_table("astronomy")
