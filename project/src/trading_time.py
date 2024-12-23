"""Trading time validation module."""
from datetime import datetime

import holidays


def is_trading_day(current_time: datetime) -> bool:
    """Check if the given time is during trading hours."""
    chinese_holidays = holidays.China(years=current_time.year)

    if current_time.weekday() >= 5 or current_time in chinese_holidays:
        return False

    current_hour = current_time.hour
    current_minute = current_time.minute

    trading_periods = [
        (9, 0, 11, 30),
        (13, 30, 15, 0),
        (21, 0, 23, 30)
    ]

    for start_h, start_m, end_h, end_m in trading_periods:
        if (start_h, start_m) <= (current_hour, current_minute) <= (end_h, end_m):
            return True

    return False
