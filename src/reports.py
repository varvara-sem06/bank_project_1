import json

from src.utils import filter_transactions_by_date, get_transactions_dataframe


def get_spending_by_weekday(date_str: str) -> str:
    """
    Возвращает траты по дням недели.
    """
    df = get_transactions_dataframe()
    filtered_df = filter_transactions_by_date(df, date_str)

    expenses_df = filtered_df[filtered_df["Сумма операции"] < 0].copy()
    expenses_df["День недели"] = expenses_df["Дата операции"].dt.dayofweek

    days_names = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятнница",
        5: "Суббота",
        6: "Воскреенье",
    }

    spending_by_day = expenses_df.groupby("День недели")["Сумма операции"].sum().abs()

    result = {}
    for day_num, amount in spending_by_day.items():
        day_name = days_names[day_num]
        result[day_name] = round(float(amount), 2)

    return json.dumps(result, ensure_ascii=False, indent=2)


def get_spending_by_workday(date_str: str) -> str:
    """
    Возвращает траты в рабочие дни.
    """
    df = get_transactions_dataframe()
    filtered_df = filter_transactions_by_date(df, date_str)

    expenses_df = filtered_df[filtered_df["Сумма операции"] < 0].copy()
    expenses_df["День недели"] = expenses_df["Дата операции"].dt.dayofweek

    workday_mask = expenses_df["День недели"] < 5

    workday_expenses = expenses_df[workday_mask]["Сумма операции"].sum()
    weekend_expenses = expenses_df[~workday_mask]["Сумма операции"].sum()

    result = {
        "workday_spending": round(float(abs(workday_expenses))),
        "weekend_spending": round(float(abs(weekend_expenses))),
    }

    return json.dumps(result, ensure_ascii=False, indent=2)
