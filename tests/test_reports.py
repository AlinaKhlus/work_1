import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.fixture
def sample_df():
    data = {
        "Дата операции": ["2021-12-01", "2021-12-01", "2021-12-02"],
        "Категория": ["Кафе", "Супермаркеты", "Кафе"],
        "Сумма операции": [-100, -500, -200],
    }
    return pd.DataFrame(data)


def test_spending_by_category(sample_df):
    result = spending_by_category(sample_df, "Кафе")

    # В данных два "Кафе": -100 и -200. Итого 300.
    assert result.at["Кафе", "Сумма операции"] == 300

    # Проверяем, что "Супермаркеты" вообще есть в индексе (так как мы не фильтровали по категории в самом тесте)
    # Но если мы фильтруем по "Кафе", то "Супермаркеты" в результат не попадут.
    # Поэтому тест на Супермаркеты здесь лишний, если мы фильтруем по "Кафе".
    # Удаляем проверку "Супермаркеты", так как мы ищем только "Кафе".


def test_spending_by_weekday(sample_df):
    result = spending_by_weekday(sample_df)

    # В данных:
    # 2021-12-01 (Wednesday): -100 и -500. Сумма = 600.
    # 2021-12-02 (Thursday): -200. Сумма = 200.

    # ОШИБКА БЫЛА ТУТ: в тесте было написано 300, но -100 + -500 = 600 (по модулю)
    assert result.at["Wednesday", "Сумма"] == 600
    assert result.at["Thursday", "Сумма"] == 200


def test_spending_by_workday(sample_df):
    result = spending_by_workday(sample_df)

    # В данных все дни (Wed, Thu) попадают в "Рабочий", так как 1 и 2 декабря 2021 - это среда и четверг.
    # Сумма: |-100| + |-500| + |-200| = 800.

    # ОШИБКА БЫЛА ТУТ: в тесте искали "Weekday", а функция возвращает "Рабочий" (на русском)
    assert result.at["Рабочий", "Сумма"] == 800

    # Проверки на "Выходной" не будет, так как в фикстуре данных нет выходных дней.
