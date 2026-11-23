import datetime
import logging
from functools import wraps

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def date_convert(date_str: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.warning(f"Неверный формат даты '{date_str}'. Используется заглушка.")
        return datetime.datetime(2021, 2, 13, 13, 0, 0)


def greeting(date_obj: datetime.datetime) -> str:
    hour = date_obj.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_excel_transactions(path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(path)

        # ГАРАНТИЯ: Колонка с датой всегда datetime
        if "Дата операции" in df.columns:
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

        # ГАРАНТИЯ: Сумма - число
        if "Сумма операции" in df.columns:
            df["Сумма операции"] = pd.to_numeric(df["Сумма операции"], errors="coerce").fillna(0)

        # Фильтрация
        if "Статус" in df.columns:
            df = df[df["Статус"] == "OK"]

        return df
    except Exception as e:
        logger.error(f"Ошибка чтения {path}: {e}")
        return pd.DataFrame()


def report_to_file(filename: str = "report.xlsx"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            df = func(*args, **kwargs)
            if isinstance(df, pd.DataFrame) and not df.empty:
                df.to_excel(filename, index=False)
                print(f"Отчет сохранен в {filename}")
            return df

        return wrapper

    return decorator
