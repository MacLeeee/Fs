"""Base plotting utilities."""
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
from typing import Tuple


def setup_time_axis(ax: plt.Axes) -> None:
    """Configure time axis formatting."""
    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(HourLocator(interval=1))
    ax.grid(True, alpha=0.3)


def create_figure() -> plt.Figure:
    """Create a new figure with default styling."""
    plt.style.use('seaborn')
    # Increase bottom margin to prevent x-label cutoff
    return plt.figure(figsize=(12, 8), constrained_layout=True)


def setup_subplots(fig: plt.Figure) -> Tuple[plt.Axes, plt.Axes]:
    """Create and setup subplots with proper spacing."""
    # Use GridSpec with constrained_layout for better automatic spacing
    gs = fig.add_gridspec(2, 1, height_ratios=[2, 1])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    return ax1, ax2
