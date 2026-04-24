from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd
import requests


def get_data_path() -> Path:
    """
    Возвращает правильный путь к файлу с данными.
    Ищет файл относительно корня проекта.
    """
    current_file = Path(__file__)  # путь к текущему файлу utils.py
    project_root = current_file.parent.parent  # поднимаемся на уровень выше от src

    data_path = project_root / "data" / "operations.xlsx"

    return data_path


def get_transactions_dataframe(excel_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Читает Excel-файл с транзакциями и возвращает DataFrame.
    """
    if excel_path is None:
        excel_path = get_data_path()

    excel_path = Path(excel_path)

    if not excel_path.exists():
        raise FileNotFoundError(f"Файл не найден: {excel_path}")

    df = pd.read_excel(excel_path)

    if "Дата операции" in df.columns:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    return df


def filter_transactions_by_date(df: pd.DataFrame, target_date_str: str) -> pd.DataFrame:
    """
    Функция принимает ДатаФрейм и указанную дату, фильтрует транзакции с начала
    месяца до указанной даты.
    """
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M:%S")
    start_date = target_date.replace(day=1, hour=0, minute=0, second=0)

    mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= target_date)
    return df.loc[mask]


def get_currency_rates(currencies: list) -> list:
    """
    Получает курсы валют через API и вовзращает список словарей
    с currency и rate.
    """
    rates = []

    for currency in currencies:
        try:
            url = f"https://www.cbr-xml-daily.ru/daily_json.js"
            response = requests.get(url)
            data = response.json()

            if currency == "USD":
                rate = data["Valute"]["USD"]["Value"]
            elif currency == "EUR":
                rate = data["Valute"]["EUR"]["Valute"]
            else:
                continue

            rates.append({"currency": currency, "rate": float(rate)})
        except Exception as e:
            print(f"Ошибка получения курса {currency}: {e}")
            rates.append({"currency": currency, "rate": 0.0})

    return rates


def get_stock_prices(stocks: list) -> list:
    """
    Получает цены акций через API.
    Возвращает список словарей с stock и price.
    """
    prices = []

    for stock in stocks:
        try:
            url = f"https://api.polygon.io/v2/aggs/ticker/{stock}/prev?adjusted=true"

            prices.append({"stock": stock, "price": 0.0})  # Заглушка, заменим на реальный API
        except Exception as e:
            print(f"Ошибка получения цены {stock}: {e}")
            prices.append({"stock": stock, "price": 0.0})

    return prices
