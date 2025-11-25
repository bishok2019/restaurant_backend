import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


PROVINCE_DATA_PATH = BASE_DIR / "fixtures/provinces.csv"
DISTRICT_DATA_PATH = BASE_DIR / "fixtures/districts.csv"
LOCAL_LEVEL_DATA_PATH = BASE_DIR / "fixtures/local_level.csv"
WARD_DATA_PATH = BASE_DIR / "fixtures/wards.csv"

# # with open('nepal_data.json', 'r') as file:
# with open(NEPAL_DATA_PATH, 'r') as file:
#     file_data = file.read()
# data = json.loads(file_data)
