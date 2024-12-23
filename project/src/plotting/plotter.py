import os
from datetime import datetime, time
from typing import List

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import pandas as pd

from src.config import PLOT_SAVE_DIR, TRADING_HOURS
from .base import create_figure
from .trading_plot import setup_trading_axes, plot_price_levels, plot_value


class DataPlotter:
    def __init__(self):
        """Initialize plotter and create output directory."""
        os.makedirs(PLOT_SAVE_DIR, exist_ok=True)
        plt.style.use("seaborn")

    def plot_id_data(self, df_pivot: pd.DataFrame, id_value: str) -> None:
        """
        Plot and save trading data for a specific ID.

        Args:
            df_pivot (pd.DataFrame): Multi-index DataFrame with "id" as one of the levels.
            id_value (str): ID of the data to plot.
        """
        try:
            # Extract data for the specific ID
            if id_value not in df_pivot.columns.get_level_values("id"):
                print(f"ID {id_value} not found in the data. Skipping plot.")
                return

            df_id = df_pivot.xs(key=id_value, axis=1, level="id").dropna(how="all")
            if df_id.empty:
                print(f"No data available for ID {id_value}. Skipping plot.")
                return

            # Filter and validate trading hours
            df_id = self.filter_trading_time(df_id)
            if df_id.empty:
                print(f"No valid trading time data for ID {id_value}. Skipping plot.")
                return

            # Split data into sessions
            sessions = self.split_trading_sessions(df_id)

            # Create figure and axes
            fig = create_figure()
            ax1, ax2 = setup_trading_axes(fig, id_value)

            # Plot each session
            for session_df in sessions:
                plot_price_levels(ax1, session_df)
                plot_value(ax2, session_df)

            # Adjust y-axis for readability
            ax1.yaxis.set_major_locator(MaxNLocator(nbins=8))  # Limit to 8 ticks for y-axis
            ax2.yaxis.set_major_locator(MaxNLocator(nbins=8))

            # Save plot
            save_path = os.path.join(PLOT_SAVE_DIR, f"plot_{id_value}.png")
            fig.savefig(save_path, dpi=100)
            plt.close(fig)

            print(f"Successfully saved plot for ID {id_value}: {save_path}")

        except Exception as e:
            print(f"Error plotting ID {id_value}: {str(e)}")

    @staticmethod
    def filter_trading_time(df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data to include only trading hours.

        Args:
            df (pd.DataFrame): DataFrame with a DateTime index.

        Returns:
            pd.DataFrame: Filtered DataFrame with data only within trading hours.
        """

        def is_trading_time(timestamp: datetime) -> bool:
            current_time = timestamp.time()
            return any(
                time(start_h, start_m) <= current_time <= time(end_h, end_m)
                for (start_h, start_m), (end_h, end_m) in TRADING_HOURS
            )

        return df[df.index.map(is_trading_time)]

    @staticmethod
    def split_trading_sessions(df: pd.DataFrame) -> List[pd.DataFrame]:
        """
        Split data into separate trading sessions based on time gaps.

        Args:
            df (pd.DataFrame): Filtered DataFrame with trading data.

        Returns:
            List[pd.DataFrame]: List of DataFrames, each representing a trading session.
        """
        # Calculate time differences between consecutive rows
        time_diffs = df.index.to_series().diff().dt.total_seconds().fillna(0)

        # Identify session breaks (e.g., gaps > 1 hour)
        session_breaks = time_diffs > 3600  # 3600 seconds = 1 hour
        session_ids = session_breaks.cumsum()  # Assign a session ID to each row

        # Split DataFrame into sessions
        sessions = [session_df for _, session_df in df.groupby(session_ids)]
        return sessions
