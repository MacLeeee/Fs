"""Main application module."""
from datetime import datetime
from typing import Optional

from src.config import DEFAULT_START_TIME, DEFAULT_END_TIME, PLOT_SAVE_DIR
from src.data_processor import DataProcessor
from src.data_scraper import DataScraper
from src.plotter import DataPlotter


def main(start_time: Optional[datetime] = None,
         end_time: Optional[datetime] = None) -> None:
    """Main execution function."""
    start_time = start_time or DEFAULT_START_TIME
    end_time = end_time or DEFAULT_END_TIME

    # Initialize components
    scraper = DataScraper()
    processor = DataProcessor()
    plotter = DataPlotter()

    # Generate URLs and scrape data
    urls = scraper.generate_urls(start_time, end_time)
    all_data = []

    for url in urls:
        print(f"Scraping: {url}")
        table_data = scraper.scrape_table(url)
        if table_data:
            all_data.extend(table_data)

    if not all_data:
        print("No data collected.")
        return

    # Process data
    df = processor.process_raw_data(all_data)
    if df is None:
        print("Failed to process data.")
        return

    df_pivot = processor.create_pivot_table(df)

    # Generate plots
    all_ids = df_pivot.columns.get_level_values('id').unique()
    for id_value in all_ids:
        print(f"Plotting ID: {id_value}")
        plotter.plot_id_data(df_pivot, id_value)

    print(f"All plots saved in '{PLOT_SAVE_DIR}' directory.")
    
if __name__ == "__main__":
    main()

