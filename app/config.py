import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_FILE = os.path.join(DATA_DIR, "flipkart_sample.csv")

# Model configurations
MODEL_PATH = "app/data/model/recommendation_model.joblib"
NLTK_DATA_PATH = os.path.join(BASE_DIR, "nltk_data")
MIN_DF = 1
NGRAM_RANGE = (1, 2)