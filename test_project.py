import pytest
from project import Calendar, get_days_month, create_menu, is_calendar_name_unique


def test_calendar_initialization():
    calendar = Calendar(
        name="TestCalendar",
        month="January",
        year="2021",
        days=30,
        daysmonth=1,
        calendar_data={"1": ["Meeting at 10 AM"]},
    )
    assert calendar.name == "TestCalendar"
    assert calendar.month == "January"
    assert calendar.year == "2021"
    assert calendar.days == 30
    assert calendar.daysmonth == 1


def test_month_setter():
    calendar = Calendar()
    calendar.month = "February"
    assert calendar.month == "February"

    calendar2 = Calendar()
    with pytest.raises(ValueError):
        calendar2.month = "InvalidMonth"


def test_year_setter():
    calendar = Calendar()
    calendar.year = "2020"
    assert calendar.year == "2020"

    calendar2 = Calendar()
    with pytest.raises(ValueError):
        calendar2.year = "1800"


def test_add_data_to_day():
    calendar = Calendar(
        name="TestCalendar",
        month="January",
        year="2021",
        days=30,
        daysmonth=1,
        calendar_data={"1": ["Meeting at 10 AM"]},
    )
    calendar.add_data_to_day(1, "Meeting at 10 AM")
    assert "Meeting at 10 AM" in calendar.calendar_data["1"]


def test_get_data_for_day():
    # With valid data
    calendar = Calendar(
        name="TestCalendar",
        month="January",
        year="2021",
        days=30,
        daysmonth=1,
        calendar_data={"1": ["Meeting at 10 AM"]},
    )
    calendar.add_data_to_day(1, "Meeting at 10 AM")
    assert calendar.get_data_for_day(1) == "Meeting at 10 AM"

    # Without data
    calendar2 = Calendar(
        name="TestCalendar",
        month="January",
        year="2021",
        days=30,
        daysmonth=1,
        calendar_data={"1": [""], "2": ["Meeting at 10 AM"]},
    )
    assert calendar2.get_data_for_day(1) == "No data found for day 1"


def test_get_days_month_regular_year():
    # Regular year
    assert get_days_month("2021", "February") == 28
    assert get_days_month("2021", "November") == 30
    # Leap year
    assert get_days_month("2020", "February") == 29


def test_create_menu():
    test_menu = create_menu("header", ["option 1", "option 2"])
    assert test_menu.header == "header"
    assert test_menu.options == ["option 1", "option 2"]


def test_is_calendar_name_unique():
    # Those names need to exist in 'data.json' to be able to test!
    assert is_calendar_name_unique("TestCalendar2") == True
    assert is_calendar_name_unique("TestCalendar") == False
