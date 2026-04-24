"""
Главный файл для демонстрации работы всех функций приложения.
"""
from src.views import get_main_page
from src.services import get_cashback_categories, search_by_description, search_by_phone
from src.reports import get_spending_by_weekday, get_spending_by_workday


def main():
    date_str = "2020-05-20 14:30:00"

    print("=" * 50)
    print("ГЛАВНАЯ СТРАНИЦА")
    print("=" * 50)
    print(get_main_page(date_str))

    print("\n" + "=" * 50)
    print("КЕШБЭК-КАТЕГОРИИ")
    print("=" * 50)
    print(get_cashback_categories(date_str))

    print("\n" + "=" * 50)
    print("ПОИСК ПО ОПИСАНИЮ ('магнит')")
    print("=" * 50)
    print(search_by_description(date_str, "магнит"))

    print("\n" + "=" * 50)
    print("ПОИСК ПО ТЕЛЕФОНУ")
    print("=" * 50)
    print(search_by_phone(date_str))

    print("\n" + "=" * 50)
    print("ТРАТЫ ПО ДНЯМ НЕДЕЛИ")
    print("=" * 50)
    print(get_spending_by_weekday(date_str))

    print("\n" + "=" * 50)
    print("ТРАТЫ РАБОЧИЙ/ВЫХОДНОЙ")
    print("=" * 50)
    print(get_spending_by_workday(date_str))


if __name__ == "__main__":
    main()
