import datetime

import pandas as pd

from src.utils import date_convert, greeting, read_excel_transactions


def test_date_convert():
    assert date_convert("2021-12-15 15:00:00") == datetime.datetime(2021, 12, 15, 15, 0)


def test_date_convert_error():
    result = date_convert("2021-12-15 25:00:00")
    assert result.year == 2021 and result.month == 2 and result.day == 13


def test_greeting():
    assert greeting(datetime.datetime(2021, 12, 15, 8, 0)) == "Доброе утро"
    assert greeting(datetime.datetime(2021, 12, 15, 14, 0)) == "Добрый день"
    assert greeting(datetime.datetime(2021, 12, 15, 20, 0)) == "Добрый вечер"
    assert greeting(datetime.datetime(2021, 12, 15, 0, 0)) == "Доброй ночи"


def test_read_excel_success(tmp_path):
    data = {
        "Дата операции": ["2021-12-01", "2021-12-02"],
        "Категория": ["Кафе", "Супермаркеты"],
        "Сумма операции": [-100, -500],
    }
    df_original = pd.DataFrame(data)  # <-- Теперь pd импортирован
    file_path = tmp_path / "test.xlsx"
    df_original.to_excel(file_path, index=False)

    df_read = read_excel_transactions(str(file_path))

    assert not df_read.empty
    assert df_read["Сумма операции"].iloc[0] == -100
    assert str(df_read["Дата операции"].dtype).startswith("datetime64")
