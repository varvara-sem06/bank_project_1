import json
from unittest.mock import patch, MagicMock
import pandas as pd
from src.services import search_by_description, get_cashback_categories, search_by_phone


@patch('src.services.get_transactions_dataframe')
@patch('src.services.filter_transactions_by_date')
def test_get_cashback_categories(mock_filter, mock_get_df):
    data = {
        'Сумма операции': [-1000, -500, -2000, 1000],
        'Категория': ['Еда', 'Еда', 'Транспорт', 'Еда'],
    }
    df = pd.DataFrame(data)
    mock_get_df.return_value = df
    mock_filter.return_value = df

    result = get_cashback_categories("2020-05-20 14:30:00")
    result_dict = json.loads(result)
    assert len(result_dict) > 0


@patch('src.services.get_transactions_dataframe')
@patch('src.services.filter_transactions_by_date')
def test_search_by_description(mock_filter, mock_get_df):
    data = {
        'Дата операции': pd.to_datetime(['2020-05-01', '2020-05-02']),
        'Сумма операции': [-1000, -500],
        'Категория': ['Еда', 'Транспорт'],
        'Описание': ['Магнит на Ленина', 'Автобус']
    }
    df = pd.DataFrame(data)
    mock_get_df.return_value = df
    mock_filter.return_value = df

    result = search_by_description("2020-05-20 14:30:00", "магнит")
    data = json.loads(result)
    assert len(data) == 1
    assert "Магнит" in data[0]['description']


@patch('src.services.get_transactions_dataframe')
@patch('src.services.filter_transactions_by_date')
def test_search_case_insensitive(mock_filter, mock_get_df):
    data = {
        'Дата операции': pd.to_datetime(['2020-05-01']),
        'Сумма операции': [-1000],
        'Категория': ['Еда'],
        'Описание': ['МАГНИТ']
    }
    df = pd.DataFrame(data)
    mock_get_df.return_value = df
    mock_filter.return_value = df

    result = search_by_description("2020-05-20 14:30:00", "магнит")
    data = json.loads(result)
    assert len(data) == 1


@patch('src.services.get_transactions_dataframe')
@patch('src.services.filter_transactions_by_date')
def test_search_by_phone(mock_filter, mock_get_df):
    data = {
        'Дата операции': pd.to_datetime(['2020-05-01']),
        'Сумма операции': [-1000],
        'Категория': ['Перевод'],
        'Описание': ['Перевод на +79001234567']
    }
    df = pd.DataFrame(data)
    mock_get_df.return_value = df
    mock_filter.return_value = df
    
    result = search_by_phone("2020-05-20 14:30:00")
    data = json.loads(result)
    assert len(data) == 1
