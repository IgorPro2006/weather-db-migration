# Завантаження датасету Global Weather Repository з Kaggle у папку data/
#   python download_data.py
import shutil
from pathlib import Path

import kagglehub

DATASET = "nelgiriyewithana/global-weather-repository"
FILE_NAME = "GlobalWeatherRepository.csv"
target = Path(__file__).parent / "data" / FILE_NAME

print("Завантаження з Kaggle... (файл великий, це може зайняти кілька хвилин)")
downloaded = kagglehub.dataset_download(DATASET, path=FILE_NAME)
shutil.copy(downloaded, target)
print(f"Готово: {target}")
