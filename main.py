# Рівень представлення: консольні команди.
#   python main.py import data/GlobalWeatherRepository.csv
#   python main.py search Ukraine 2024-05-16
#   python main.py search Ukraine 2024-05-16 Kyiv
import sys
from datetime import date

from weather_app import services

args = sys.argv[1:]

if len(args) == 2 and args[0] == "import":
    services.import_csv(args[1])
elif len(args) in (3, 4) and args[0] == "search":
    city = args[3] if len(args) == 4 else None
    services.search(args[1], date.fromisoformat(args[2]), city)
else:
    print("Використання:")
    print("  python main.py import <файл.csv>")
    print("  python main.py search <країна> <РРРР-ММ-ДД> [місто]")
