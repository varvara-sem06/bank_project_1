import pandas as pd
from pathlib import Path
from src.utils import filter_transactions_by_date, get_data_path


def test_get_data_path():
    path = get_data_path()
    assert isinstance(path, Path)
    assert path.name == "operations.xlsx"


def test_filter_transactions_by_date():
    data = {
        'Дата операции': pd.to_datetime(['2020-05-01', '2020-05-15', '2020-05-25']),
        'Сумма операции': [-1000, -500, -200],
    }
    df = pd.DataFrame(data)

    result = filter_transactions_by_date(df, "2020-05-20 14:30:00")
    assert len(result) == 2


def test_filter_transactions_by_date_all_month():
    data = {
        'Дата операции': pd.to_datetime(['2020-05-01', '2020-05-31']),
        'Сумма операции': [-1000, -500],
    }
    df = pd.DataFrame(data)

    result = filter_transactions_by_date(df, "2020-05-31 23:59:00")
    assert len(result) == 2
