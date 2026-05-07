import json
from src.reports import get_spending_by_weekday, get_spending_by_workday


def test_weekday_report_is_json():
    result = get_spending_by_weekday("2020-05-20 14:30:00")
    data = json.loads(result)
    assert isinstance(data, dict)


def test_workday_report_has_keys():
    result = get_spending_by_workday("2020-05-20 14:30:00")
    data = json.loads(result)
    assert "workday_spending" in data
    assert "weekend_spending" in data
