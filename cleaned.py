import datetime
import sys
import calendar
import re
import json
from tabulate import tabulate
import pyfiglet
import os
import jsonlines

class Calendar:
    MONTH_REGEX = r"^(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)$"
    YEAR_REGEX = r"^(19|20)\d{2}$"

    def __init__(self, name="", month="January", year="1900", daysmonth=0, calendar_data={}):
        self.name = name
        self._month = month
        self._year = year
        self._daysmonth = daysmonth
        self.calendar_data = calendar_data

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, month):
        if not re.search(self.MONTH_REGEX, month, re.IGNORECASE):
            raise ValueError("Invalid Month")
        self._month = month

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if not re.search(self.YEAR_REGEX, year, re.IGNORECASE):
            raise ValueError("Invalid Year")
        self._year = year

    @property
    def daysmonth(self):
        return self._daysmonth

    @daysmonth.setter
    def daysmonth(self, daysmonth):
        tDays = get_days_month(self.year, self.month)
        if tDays < int(daysmonth):
            raise ValueError("More days than the month has!")
        self._daysmonth = int(daysmonth)

    def get_valid_input(self, prompt, setter_attr):
        while True:
            try:
                user_input = input(prompt)
                setattr(self, setter_attr, user_input)
                return user_input
            except ValueError as e:
                print(e)

    def get_data_for_day(self, day):
        day = str(day)
        if day in self.calendar_data:
            data = self.calendar_data[day]
            if data != [""]:
                print(f"Data for day {day} in calendar {self.name}: {', '.join(data)}")
            else:
                print(f"No data found for day {day}")
        else:
            print(f"No data stored for day {day}")

    def generate_month_table(self):
        header = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        num_days = get_days_month(self.year, self.month) if not self.daysmonth else int(self.daysmonth)
        first_day = datetime.datetime(int(self.year), datetime.datetime.strptime(self.month, "%B").month, 1).weekday()

        calendar_table = [["" for _ in range(7)]]
        current_row = calendar_table[0]

        for day in range(1, num_days + 1):
            day_str = str(day)
            day_data_indicator = "!" if day_str in self.calendar_data and self.calendar_data[day_str] != [""] else ""
            current_row[(day + first_day) % 7] = f"{day}{day_data_indicator}"

            if (day + first_day) % 7 == 6:
                calendar_table.append(["" for _ in range(7)])
                current_row = calendar_table[-1]

        print(f"\n****'!' marks days that contain data****")
        print(f"Calendar '{self.name}' for {self.month}, {self.year}")
        print(tabulate(calendar_table, headers=header, tablefmt="fancy_grid"))

    def add_data_to_day(self, day, data):
        if day < 1 or day > self.daysmonth:
            raise ValueError("Invalid day")
        self.calendar_data.setdefault(day, []).append(data)

    def save_to_json(self):
        path = "data.json"
        updated = False
        all_calendars = []

        try:
            with jsonlines.open(path, mode="r") as reader:
                all_calendars = [calendar if calendar["name"] != self.name else self.__dict__ for calendar in reader]
                updated = any(calendar["name"] == self.name for calendar in all_calendars)
        except FileNotFoundError:
            pass

        if not updated:
            all_calendars.append(self.__dict__)

        with jsonlines.open(path, mode="w") as writer:
            writer.write_all(all_calendars)

    @staticmethod
    def is_calendar_name_unique(name):
        try:
            with open("data.json", "r") as file:
                return not any(json.loads(line)["name"] == name for line in file)
        except FileNotFoundError:
            return True

    def update_calendar_data(self, data):
        self.calendar_data = data

    def edit_data_for_day(self):
        print(self.name)
        while True:
            try:
                day_select = int(input("Data of which day to edit? "))
                if day_select < 1 or day_select > self._daysmonth:
                    raise ValueError("Invalid day")
                self.calendar_data[str(day_select)] = [input("New data: ")]
                break
            except ValueError as e:
                print(e)

        self.save_to_json()
        return self.calendar_data

class Menu:
    OPTION_QUIT = "q"

    def __init__(self, header, options, instructions):
        self.options = options
        self.header = header
        self.options_count = len(options)
        self.instructions = instructions

    def display_menu(self):
        print(self.instructions)
        table = [[index, option] for index, option in enumerate(self.options, start=1)]
        print(tabulate(table, headers=["Option", "Action"], tablefmt="fancy_grid"))

    def get_selection(self):
        while True:
            try:
                user_input = input("Enter number: ")
                selected_option = int(user_input)
                if 0 < selected_option <= self.options_count:
                    return selected_option
                else:
                    raise ValueError
            except ValueError:
                print("Invalid option, please enter a number within the options range.")
                self.display_menu()

    def get_header(self):
        print(pyfiglet.figlet_format(self.header))

def create_menu(header, options=[]):
    return Menu(header, options, "****Choose an option!****")

def create_new_calendar():
    adCalendar = Calendar()
    get_calendar_input(adCalendar)
    adCalendar.generate_month_table()
    save_menu = create_menu("Save", ["Save calendar", "Back to main menu"])
    save_menu.display_menu()
    user_input_save = save_menu.get_selection()

    if user_input_save == 1:
        adCalendar.save_to_json()
        print("Calendar saved successfully.")
    elif user_input_save == Menu.OPTION_QUIT:
        sys.exit("Exiting Application")

def print_available_calendars():
    print("***Available calendars***")
    adCalendar = read_json()
    return adCalendar

def read_json(silent="n", selector=""):
    calendar_data = {}
    try:
        with open("data.json", "r") as file:
            for line in file:
                calendar = json.loads(line)
                calendar_data[calendar["name"]] = calendar

        if silent != "y":
            print("***Available calendars***")
            calendar_data_list = [(index, name) for index, name in enumerate(calendar_data, start=1)]
            print(tabulate(calendar_data_list, headers=["Index", "Calendar Name"], tablefmt="fancy_grid"))
            selector = input("Which calendar do you want to load? Enter Calendar Name: ")

        selected_calendar = calendar_data.get(selector)
        if selected_calendar:
            adCalendar = Calendar(
                selected_calendar["name"],
                selected_calendar["_month"],
                selected_calendar["_year"],
                selected_calendar["_daysmonth"],
                selected_calendar["calendar_data"],
            )
            return adCalendar
        else:
            print(f"Calendar '{selector}' does not exist.")
            return None
    except FileNotFoundError:
        print("File 'data.json' not found.")
        return None

def get_calendar_input(adCalendar):
    adCalendar.name = adCalendar.get_valid_input("What do you want to call this calendar? ", "name")
    adCalendar.year = adCalendar.get_valid_input("For which year do you want to generate a calendar? ", "year")
    adCalendar.month = adCalendar.get_valid_input("For which month do you want to generate a calendar? ", "month")

    use_default_input = input(f"Do you want to use the default amount of days for this month ({get_days_month(adCalendar.year, adCalendar.month)}) [Y/n]? ").lower()
    while not re.match(r"^[yn]$", use_default_input):
        print("Invalid input. Please enter 'Y' or 'N'.")
        use_default_input = input(f"Do you want to use the default amount of days for this month ({get_days_month(adCalendar.year, adCalendar.month)}) [Y/n]? ").lower()

    if use_default_input == "n":
        adCalendar.daysmonth = adCalendar.get_valid_input(f"For how many days do you want to run the calendar in {adCalendar.month}? ", "daysmonth")
        enter_data(adCalendar, int(adCalendar.daysmonth))
    else:
        enter_data(adCalendar, get_days_month(adCalendar.year, adCalendar.month))

def enter_data(calendar, daysmonth):
    for day in range(1, daysmonth + 1):
        data = input(f"Enter data for day {day}: ")
        calendar.add_data_to_day(day, data)

def get_days_month(year, month):
    date_format = "%B"
    date_object = datetime.datetime.strptime(month, date_format)
    return calendar.monthrange(int(year), date_object.month)[1]

def main():
    menu = create_menu("AdCalendar", ["Create a new calendar", "Load an existing calendar", "Quit"])
    menu.get_header()
    while True:
        menu.display_menu()
        user_input = menu.get_selection()
        if user_input == 1:
            create_new_calendar()
        elif user_input == 2:
            adCalendar = print_available_calendars()
            if adCalendar:
                save_menu = create_menu("Save", ["Read entry", "Edit entry", "Back to main menu"])
                while True:
                    adCalendar.generate_month_table()
                    save_menu.display_menu()
                    user_input_dialogue = save_menu.get_selection()
                    if user_input_dialogue == 1:
                        user_day = input("For which day do you want to read the data? Enter number: ")
                        adCalendar.get_data_for_day(int(user_day))
                    elif user_input_dialogue == 2:
                        day_data = adCalendar.edit_data_for_day()
                        adCalendar.update_calendar_data(day_data)
                    elif user_input_dialogue == Menu.OPTION_QUIT:
                        break
        elif user_input == Menu.OPTION_QUIT:
            sys.exit("Exiting Application")

if __name__ == "__main__":
    main()

