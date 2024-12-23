"""Data visualization module."""
import os

from matplotlib.dates import DateFormatter, HourLocator
import matplotlib.pyplot as plt
import pandas as pd

from src.config import PLOT_SAVE_DIR


def _setup_axes(fig: plt.Figure, id_value: str) -> tuple:
    """设置图表轴和基本样式。"""
    # 创建子图，设置合适的间距
    gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.3)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # 设置标题
    fig.suptitle(f"ID: {id_value} - Trading Data", y=0.95)

    # 配置x轴时间格式
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
        ax.xaxis.set_major_locator(HourLocator(interval=1))
        ax.grid(True, alpha=0.3)

    return ax1, ax2


def _plot_data(ax1: plt.Axes, ax2: plt.Axes, df_id: pd.DataFrame) -> None:
    """绘制数据到指定轴。"""
    # 绘制s、m、l曲线
    for col, color, label in zip(
            ["s", "m", "l"],
            ["#1f77b4", "#ff7f0e", "#2ca02c"],
            ["Short", "Medium", "Long"]
    ):
        ax1.plot(df_id.index, df_id[col], label=label, color=color, linewidth=1.5)
    ax1.set_ylabel("Price Levels")
    ax1.legend(loc='upper left')

    # 绘制y曲线
    ax2.plot(df_id.index, df_id["y"], label="Value", color="#d62728", linewidth=1.5)
    ax2.set_ylabel("Value")
    ax2.legend(loc='upper left')


class DataPlotter:
    def __init__(self):
        """Initialize plotter and create output directory."""
        os.makedirs(PLOT_SAVE_DIR, exist_ok=True)
        plt.style.use('seaborn')  # 使用更现代的样式

    @staticmethod
    def plot_id_data(df_pivot: pd.DataFrame, id_value: str) -> None:
        """为指定ID绘制并保存图表。"""
        try:
            # 提取数据
            df_id = df_pivot.xs(key=id_value, axis=1, level="id")
            if df_id.empty:
                print(f"No data available for ID: {id_value}")
                return

            # 过滤和清理数据
            df_id = filter_trading_time(df_id.dropna(how="all"))
            if df_id.empty:
                print(f"No valid trading time data for ID: {id_value}")
                return

            # 创建图表
            fig = plt.figure(figsize=(12, 8), dpi=100)
            ax1, ax2 = _setup_axes(fig, id_value)

            # 绘制数据
            _plot_data(ax1, ax2, df_id)

            # 调整布局并保存
            fig.set_tight_layout(True)
            save_path = os.path.join(PLOT_SAVE_DIR, f"plot_{id_value}.png")
            fig.savefig(save_path, bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

            print(f"Successfully saved plot for ID {id_value}")

        except Exception as e:
            print(f"Error plotting ID {id_value}: {str(e)}")


def filter_trading_time(df: pd.DataFrame) -> pd.DataFrame:
    """过滤交易时间数据。"""

    def is_trading_time(timestamp):
        time = timestamp.time()
        return (
                (pd.to_datetime("09:00").time() <= time <= pd.to_datetime("15:00").time()) or
                (pd.to_datetime("21:00").time() <= time <= pd.to_datetime("23:30").time())
        )

    return df[df.index.map(is_trading_time)]
