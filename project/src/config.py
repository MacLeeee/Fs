"""Configuration settings for the application."""
from datetime import datetime

# API Configuration
BASE_URL = "http://150.158.125.175:8080/QH20D/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/114.0.0.0 '
                  'Safari/537.36 '
}

# Time Configuration
TRADING_HOURS = [
    ((9, 0), (11, 30)),
    ((13, 30), (15, 0)),
    ((21, 0), (23, 30))
]

# Data Configuration
COLUMNS_TO_KEEP = ["date", "id", "y", "l", "m", "s"]
PLOT_SAVE_DIR = "plots"

# Default date range
DEFAULT_START_TIME = datetime.strptime("2024-08-27 09:00:00", "%Y-%m-%d %H:%M:%S")
DEFAULT_END_TIME = datetime.strptime('2024-08-27 23:00:00', "%Y-%m-%d %H:%M:%S")
