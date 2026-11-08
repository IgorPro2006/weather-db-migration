"""Етап 1: створення таблиці weather"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None

WIND_DIRECTIONS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                   "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
wind_direction_enum = sa.Enum(*WIND_DIRECTIONS, name="wind_direction_enum")


def upgrade():
    op.create_table(
        "weather",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("location_name", sa.String(100), nullable=False),
        sa.Column("last_updated", sa.DateTime, nullable=False),
        sa.Column("temperature_celsius", sa.Double),
        sa.Column("condition_text", sa.String(100)),
        sa.Column("humidity", sa.Integer),
        sa.Column("wind_kph", sa.Double),
        sa.Column("wind_degree", sa.Integer),
        sa.Column("wind_direction", wind_direction_enum),
        sa.Column("sunrise", sa.Time),
        sa.Column("sunset", sa.Time),
        sa.Column("moonrise", sa.Time),
        sa.Column("moonset", sa.Time),
        sa.Column("moon_phase", sa.String(20)),
        sa.Column("moon_illumination", sa.Integer),
    )


def downgrade():
    op.drop_table("weather")
    wind_direction_enum.drop(op.get_bind(), checkfirst=True)  # тип ENUM у Postgres
