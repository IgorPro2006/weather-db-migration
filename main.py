# Рівень представлення: консольні команди.
#   python main.py import data/GlobalWeatherRepository.csv
import sys

from weather_app import services

if len(sys.argv) == 3 and sys.argv[1] == "import":
    services.import_csv(sys.argv[2])
else:
    print("Використання:")
    print("  python main.py import <файл.csv>")
