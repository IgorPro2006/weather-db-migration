# ORM-модель: опис таблиць БД у вигляді Python-класів.
# Етап 2: дані про схід-захід небесних тіл винесено в окрему таблицю astronomy.
from sqlalchemy import Column, DateTime, Double, Enum, ForeignKey, Integer, String, Time
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

WIND_DIRECTIONS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                   "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    country = Column(String(100), nullable=False)          # текст
    location_name = Column(String(100), nullable=False)
    last_updated = Column(DateTime, nullable=False)        # дата (і час)
    temperature_celsius = Column(Double)
    condition_text = Column(String(100))
    humidity = Column(Integer)
    wind_kph = Column(Double)                              # дробове число
    wind_degree = Column(Integer)                          # ціле число
    wind_direction = Column(Enum(*WIND_DIRECTIONS, name="wind_direction_enum"))  # enum

    # один запис weather <-> один запис astronomy
    astronomy = relationship("Astronomy", uselist=False, back_populates="weather")


class Astronomy(Base):
    """Категорія варіанту 16: схід-захід небесних тіл."""
    __tablename__ = "astronomy"

    id = Column(Integer, primary_key=True)
    weather_id = Column(Integer, ForeignKey("weather.id"), nullable=False, unique=True)
    sunrise = Column(Time)                                 # час
    sunset = Column(Time)
    moonrise = Column(Time)
    moonset = Column(Time)
    moon_phase = Column(String(20))
    moon_illumination = Column(Integer)

    weather = relationship("Weather", back_populates="astronomy")
