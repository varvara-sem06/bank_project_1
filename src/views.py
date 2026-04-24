import json
from datetime import datetime
from typing import Any

from src.utils import filter_transactions_by_date, get_currency_rates, get_stock_prices, get_transactions_dataframe


def get_greeting(time_info: str) -> str:
    """
    Функция принимает строку с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'
    и возвращает приветствие в зависимости от времени суток.
    """
    dt = datetime.strptime(time_info, "%Y-%m-%d %H:%M:%S")
    hour = dt.hour

    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards_info(df):
    """
    Возввращает информацию по каждой карте:
    - последние 4 цифра карты
    - общая сумма расходов
    - кешбэк
    """
    cards_data = []
    cards = df["Номер карты"].dropna().unique()
    for card in cards:
        card_df = df[df["Номер карты"] == card]

        expenses = card_df[card_df["Сумма операции"] < 0]["Сумма операции"].abs().sum()

        cashback = expenses / 100

        cards_data.append(
            {"last_digits": str(card)[-4:], "total_spent": round(expenses, 2), "cashback": round(cashback, 2)}
        )

    return cards_data


def get_top_transactions(df, top_n=5):
    """
    Генерирует топ транзакций по сумме платежа по убыванию.
    """
    top_df = df.nlargest(top_n, "Сумма платежа")

    transactions = []
    for _, row in top_df.iterrows():
        transactions.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": row["Сумма операции"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return transactions


def load_user_settings(settings_path: str = "../user_settings.json") -> Any:
    """
    Загружает пользовательские настройки из JSON-файла и возвращает
    словарь с валютами и акциями.
    """
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    return settings


def get_main_page(date_str: str):
    """
    Главная функция для формирования JSON-ответа главной страницы.
    """
    df = get_transactions_dataframe()

    filtered_df = filter_transactions_by_date(df, date_str)

    response = {
        "greeting": get_greeting(date_str),
        "cards": get_cards_info(filtered_df),
        "top_transactions": get_top_transactions(filtered_df),
        "currency_rates": get_currency_rates,
        "stock_prices": get_stock_prices,
    }

    return response
