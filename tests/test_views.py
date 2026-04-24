import json
from unittest.mock import patch, MagicMock
import pandas as pd
from src.views import get_greeting, get_cards_info, get_top_transactions


def test_get_greeting_morning():
    assert "Доброе утро" in get_greeting("2020-05-20 08:00:00")


def test_get_greeting_day():
    assert "Добрый день" in get_greeting("2020-05-20 14:00:00")


def test_get_greeting_evening():
    assert "Добрый вечер" in get_greeting("2020-05-20 20:00:00")


def test_get_greeting_night():
    assert "Доброй ночи" in get_greeting("2020-05-20 02:00:00")


def test_get_greeting_boundaries():
    assert "Доброе утро" in get_greeting("2020-05-20 06:00:00")
    assert "Добрый день" in get_greeting("2020-05-20 12:00:00")
    assert "Добрый вечер" in get_greeting("2020-05-20 18:00:00")
    assert "Доброй ночи" in get_greeting("2020-05-20 23:00:00")


def test_get_cards_info():
    data = {
        'Номер карты': ['*4556', '*4556', '*7890'],
        'Сумма операции': [-1000, -500, -200],
    }
    df = pd.DataFrame(data)
    result = get_cards_info(df)
    assert len(result) == 2
    assert result[0]['last_digits'] == '4556'
    assert result[0]['total_spent'] == 1500.0
    assert result[0]['cashback'] == 15.0


def test_get_top_transactions():
    data = {
        'Дата операции': pd.to_datetime(['2020-05-01', '2020-05-02', '2020-05-03']),
        'Сумма операции': [-1000, -5000, -2000],
        'Сумма платежа': [-1000, -5000, -2000],
        'Категория': ['Еда', 'Транспорт', 'Еда'],
        'Описание': ['Магнит', 'Автобус', 'Пятерочка']
    }
    df = pd.DataFrame(data)
    result = get_top_transactions(df)
    assert len(result) == 3
