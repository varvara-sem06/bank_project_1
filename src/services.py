import json

from src.utils import filter_transactions_by_date, get_transactions_dataframe


def get_cashback_categories(date_str: str) -> str:
    """
    Возвращает JSON с топ категориями по кешбеку.
    """
    df = get_transactions_dataframe()

    filtered_df = filter_transactions_by_date(df, date_str)

    expenses_df = filtered_df[filtered_df["Сумма операции"] < 0].copy()

    expenses_by_category = expenses_df.groupby("Категория")["Сумма операции"].sum().abs()

    cashback_by_category = expenses_by_category / 100

    cashback_sorted = cashback_by_category.sort_values(ascending=False)

    cashback_rounded = cashback_sorted.round(0).astype(int)

    result = {}
    for category, cashback in cashback_rounded.head(3).items():
        result[category] = cashback
    return json.dumps(result, ensure_ascii=False, indent=2)


def search_by_phone(date_str: str) -> str:
    """
    Ищет транзакции по номеру телефона.
    """
    df = get_transactions_dataframe()

    filtered_df = filter_transactions_by_date(df, date_str)

    phone_pattern = r"(\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"

    mask = filtered_df["Описание"].str.contains(phone_pattern, regex=True, na=False)

    results_df = filtered_df[mask]

    results_list = []
    for _, row in results_df.iterrows():
        results_list.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": row["Сумма операции"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    return json.dumps(results_list, ensure_ascii=False, indent=2)


def search_by_description(date_str: str, search_query: str) -> str:
    """
    Ищет транзакции по тексту в описании или подстроке.
    """
    df = get_transactions_dataframe()

    filtered_df = filter_transactions_by_date(df, date_str)

    mask = filtered_df["Описание"].str.lower().str.contains(search_query.lower())

    results_df = filtered_df[mask]

    results_list = []
    for _, row in results_df.iterrows():
        results_list.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": row["Сумма операции"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return json.dumps(results_list, ensure_ascii=False, indent=2)
