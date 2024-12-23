"""Trading data specific plotting functions."""
import matplotlib.pyplot as plt
import pandas as pd
from typing import Tuple
from matplotlib.ticker import MaxNLocator
from .base import setup_time_axis


def setup_trading_axes(fig: plt.Figure, id_value: str) -> Tuple[plt.Axes, plt.Axes]:
    """
    Setup axes for trading data plots.

    Args:
        fig (plt.Figure): Matplotlib figure object.
        id_value (str): Identifier for the data being plotted.

    Returns:
        Tuple[plt.Axes, plt.Axes]: Two axes for price levels and value.
    """
    from .base import setup_subplots

    ax1, ax2 = setup_subplots(fig)
    fig.suptitle(f"ID: {id_value} - Trading Data", y=0.98)

    for ax in [ax1, ax2]:
        setup_time_axis(ax)
        # Add padding to y-axis
        ax.margins(y=0.1)

    return ax1, ax2


def plot_price_levels(ax: plt.Axes, df: pd.DataFrame) -> None:
    """
    Plot price level data (s, m, l).

    Args:
        ax (plt.Axes): Matplotlib Axes object.
        df (pd.DataFrame): DataFrame containing price level data.
    """
    for col, color, label in zip(
            ["s", "m", "l"],
            ["#1f77b4", "#ff7f0e", "#2ca02c"],
            ["Short", "Medium", "Long"]
    ):
        ax.plot(df.index, df[col], label=label, color=color, linewidth=1.5)

    ax.set_ylabel("Price Levels")
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1.02))

    # Optimize y-axis ticks
    ax.yaxis.set_major_locator(MaxNLocator(nbins=8))  # Limit to 8 ticks for better readability


def plot_value(ax: plt.Axes, df: pd.DataFrame) -> None:
    """
    Plot y value data.

    Args:
        ax (plt.Axes): Matplotlib Axes object.
        df (pd.DataFrame): DataFrame containing value data.
    """
    ax.plot(df.index, df["y"], label="Value", color="#d62728", linewidth=1.5)
    ax.set_ylabel("Value")
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1.02))

    # Optimize y-axis ticks
    ax.yaxis.set_major_locator(MaxNLocator(nbins=8))  # Limit to 8 ticks for better readability
