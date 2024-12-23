"""Data processing module."""
import pandas as pd
from typing import List, Optional


class DataProcessor:
    @staticmethod
    def process_raw_data(data: List[List[str]]) -> Optional[pd.DataFrame]:
        """Process raw data into a DataFrame."""
        if not data:
            return None

        df = pd.DataFrame(data)
        df = df.iloc[:, [0, 1, 3, 20, 21, 22]]
        df.columns = ["date", "id", "y", "l", "m", "s"]
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        return df

    @staticmethod
    def create_pivot_table(df: pd.DataFrame) -> pd.DataFrame:
        """Create pivot table from processed data."""
        return df.pivot_table(
            index="date",
            columns="id",
            values=["y", "l", "m", "s"],
            aggfunc="first"
        )
