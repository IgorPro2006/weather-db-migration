# Читання CSV-файлу датасету. З кожного рядка беремо лише колонки,
# описані в ORM-моделі, і перетворюємо текст у потрібні типи.
import csv
from datetime import datetime

from weather_app.models import WIND_DIRECTIONS


def to_float(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def to_int(text):
    value = to_float(text)
    return None if value is None else int(value)


def to_time(text):
    # "06:04 AM" -> 06:04; "No moonrise" -> None
    try:
        return datetime.strptime(text.strip(), "%I:%M %p").time()
    except (AttributeError, ValueError):
        return None


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            direction = row.get("wind_direction")
            yield {
                "country": row["country"],
                "location_name": row["location_name"],
                "last_updated": datetime.strptime(row["last_updated"], "%Y-%m-%d %H:%M"),
                "temperature_celsius": to_float(row.get("temperature_celsius")),
                "condition_text": row.get("condition_text"),
                "humidity": to_int(row.get("humidity")),
                "wind_kph": to_float(row.get("wind_kph")),
                "wind_degree": to_int(row.get("wind_degree")),
                "wind_direction": direction if direction in WIND_DIRECTIONS else None,
                "sunrise": to_time(row.get("sunrise")),
                "sunset": to_time(row.get("sunset")),
                "moonrise": to_time(row.get("moonrise")),
                "moonset": to_time(row.get("moonset")),
                "moon_phase": row.get("moon_phase"),
                "moon_illumination": to_int(row.get("moon_illumination")),
            }
