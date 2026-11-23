import pandas as pd

from src.utils import report_to_file


@report_to_file(filename="spending_by_category.xlsx")
def spending_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    Группирует траты по категории и возвращает DataFrame.
    """
    # Фильтруем по вхождению строки (case-insensitive)
    mask = df["Категория"].str.lower().str.contains(category.lower(), na=False)
    filtered = df[mask]

    result = (
        filtered.groupby("Категория")["Сумма операции"]
        .sum()
        .abs()
        .sort_values(ascending=False)
        .to_frame(name="Сумма операции")
    )
    return result


@report_to_file(filename="spending_by_weekday.xlsx")
def spending_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    """
    Группирует траты по дням недели.
    """
    # Гарантируем, что колонка с датой - это datetime
    if df["Дата операции"].dtype != "datetime64[ns]":
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

    df["День недели"] = df["Дата операции"].dt.day_name()

    result = (
        df.groupby("День недели")["Сумма операции"].sum().abs().sort_values(ascending=False).to_frame(name="Сумма")
    )
    return result


@report_to_file(filename="spending_by_workday.xlsx")
def spending_by_workday(df: pd.DataFrame) -> pd.DataFrame:
    if df["Дата операции"].dtype != "datetime64[ns]":
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")

    # ИСПРАВЛЕНО: .dt.day_of_week вместо .dt.weekday
    df["Тип дня"] = df["Дата операции"].dt.day_of_week.apply(lambda x: "Выходной" if x >= 5 else "Рабочий")

    result = df.groupby("Тип дня")["Сумма операции"].sum().abs().to_frame(name="Сумма")
    return result
