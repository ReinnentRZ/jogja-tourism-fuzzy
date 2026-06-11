from functools import lru_cache
from pathlib import Path
import pandas as pd

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

CSV_PATH_PARIWISATA = PROJECT_ROOT / "dataset" / "clean" / "data_pariwisata_clean.csv"
CSV_PATH_WISATA_FINAL = PROJECT_ROOT / "dataset" / "clean" / "data_wisata_clean.csv"

@lru_cache(maxsize=None)
def pariwisata():
    return pd.read_csv(CSV_PATH_PARIWISATA)
