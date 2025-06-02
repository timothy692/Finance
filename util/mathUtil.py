from datetime import datetime

def get_relative_date(month_delta: int) -> datetime:
    """
    Returns a date adjusted by a given number of months relative to the current date
    """

    now = datetime.now()

    adjusted_month = (now.month + month_delta - 1) % 12 + 1
    adjusted_year = now.year + (now.month + month_delta - 1) // 12

    return now.replace(year=adjusted_year, month=adjusted_month)