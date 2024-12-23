"""Data scraping module."""
from datetime import datetime, timedelta
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from src.config import BASE_URL, HEADERS
from src.trading_time import is_trading_day


class DataScraper:
    @staticmethod
    def generate_urls(start_time: datetime, end_time: datetime) -> List[str]:
        """Generate URLs for the given time range."""
        urls = []
        current_time = start_time

        while current_time <= end_time:
            if is_trading_day(current_time):
                time_str = current_time.strftime("%Y%m%d-%H%M%S")
                urls.append(f"{BASE_URL}{time_str}")
            current_time += timedelta(minutes=5)

        return urls

    @staticmethod
    def scrape_table(url: str) -> Optional[List[List[str]]]:
        """Scrape table data from the given URL."""
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')

            if not table:
                return None

            return [[cell.text.strip() for cell in row.find_all('td')]
                    for row in table.find_all('tr')
                    if row.find_all('td')]

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
