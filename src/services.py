import logging

import pandas as pd

from src.utils import report_to_file

logger = logging.getLogger(__name__)


@report_to_file(filename="cards_statistic.xlsx")
def cards_statistic(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    expenses = df[df["Сумма операции"] < 0]
    if expenses.empty:
        return pd.DataFrame()

    grouped = expenses.groupby(df["Номер карты"].str[-4:])["Сумма операции"].sum()

    result = pd.DataFrame(
        {
            "last_digits": grouped.index,
            "total_spent": grouped.abs(),
            "cashback": expenses.groupby(df["Номер карты"].str[-4:])["Кэшбэк"].sum(),
        }
    ).sort_values("total_spent", ascending=False)

    return result


@report_to_file(filename="top5_transactions.xlsx")
def top5_transactions(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    sorted_df = df.sort_values("Сумма операции", key=abs, ascending=False)

    # ВАЖНО: Берем только те колонки, которые ЕСТЬ в df
    cols = ["Дата операции", "Категория", "Сумма операции"]
    if "Описание" in df.columns:
        cols.append("Описание")

    return sorted_df.head(5)[cols]
