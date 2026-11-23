import pandas as pd
import pytest

from src.services import cards_statistic, top5_transactions


@pytest.fixture
def sample_df_services():
    data = {
        "Дата операции": ["2021-12-01", "2021-12-01", "2021-12-02"],
        "Категория": ["Кафе", "Супермаркеты", "Кафе"],
        "Сумма операции": [-100, -500, -200],
        "Номер карты": ["*1111", "*2222", "*1111"],
        "Кэшбэк": [1, 5, 2],
    }
    return pd.DataFrame(data)


def test_cards_statistic(sample_df_services):
    result = cards_statistic(sample_df_services)
    assert result.at["1111", "total_spent"] == 300
    assert result.at["2222", "total_spent"] == 500
    assert result.at["1111", "cashback"] == 3
    assert result.at["2222", "cashback"] == 5


def test_top5_transactions(sample_df_services):
    result = top5_transactions(sample_df_services)
    assert len(result) == 3
    # ИСПРАВЛЕНО: ищем максимальный модуль суммы
    assert result["Сумма операции"].abs().max() == 500
