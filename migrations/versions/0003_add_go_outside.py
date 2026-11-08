"""Етап 3: колонка go_outside - "Чи варто виходити на вулицю"

Формула: виходити варто, якщо в момент спостереження (час з weather.last_updated)
надворі день - Сонце вже зійшло і ще не зайшло.
"""
import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"


def upgrade():
    # 1. додаємо колонку, поки що порожню
    op.add_column("astronomy", sa.Column("go_outside", sa.Boolean, nullable=True))

    # 2. заповнюємо за формулою
    #    (якщо захід після півночі, наприклад у Рейк'явіку влітку, sunset < sunrise)
    op.execute("""
        UPDATE astronomy SET go_outside = (
            SELECT CASE
                WHEN astronomy.sunrise IS NULL OR astronomy.sunset IS NULL THEN false
                WHEN astronomy.sunrise < astronomy.sunset THEN
                     CAST(w.last_updated AS TIME) >= astronomy.sunrise
                     AND CAST(w.last_updated AS TIME) < astronomy.sunset
                ELSE CAST(w.last_updated AS TIME) >= astronomy.sunrise
                     OR CAST(w.last_updated AS TIME) < astronomy.sunset
            END
            FROM weather w
            WHERE w.id = astronomy.weather_id
        )
    """)

    # 3. забороняємо порожні значення
    op.alter_column("astronomy", "go_outside", existing_type=sa.Boolean(), nullable=False)


def downgrade():
    op.drop_column("astronomy", "go_outside")
