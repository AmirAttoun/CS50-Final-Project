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
    MONTH_REGEX = r"^(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)$"
    YEAR_REGEX = r"^(19|20)\d{2}$"

    def __init__(
        self: object,
        name="",
        month="January",
        year="1900",
        daysmonth=0,
        days=0,
        calendar_data={},
    ):
        """
        An instanced method to initialize class Calendar
        :param self: Expects instance of class Menu
        :param name: Name of the calendar
        :param month: Calendar for given month.
        :param year: Calendar for given year.
        :param daysmonth: Run time of calendar
        :param days: Days in given month.
        :param calendar_data: Data associated with certain days in calendar.
        :type self: Expects instance of class Menu
        :type name: str
        :type month: str
        :type year: str
        :type daysmonth: int
        :type days: int
        :type calendar_data: dict

        """
        self.name = name
        self.month = month
        self.year = year
        self.days = days
        self.daysmonth = daysmonth
        self.calendar_data = calendar_data

    @property
    def month(self: object) -> str:
        """
        Getter method for a month
        Gets attribute month of instance.
        :param self: Expects instance of class Calendar
        :type self: object
        :return: Month in calendar
        :rtype: str
        """
        return self._month

    @month.setter
    def month(self: object, month: str):
        """
        Setter method for a month. Validates for a correct month.
        Sets attribute month
        :param self: Expects instance of class Calendar
        :param month: Input month provided by user
        :type self: object
        :type month: str
        """
        if not re.search(self.MONTH_REGEX, month, re.IGNORECASE):
            raise ValueError("Invalid Month")
        self._month = month

    @property
    def year(self: object) -> int:
        """
        Getter method for calendar year
        Gets attribute year of instance.
        :param self: Expects instance of class Calendar
        :type self: object
        :return: Calendar year
        :rtype: str
        """
        return self._year

    @year.setter
    def year(self: object, year: str):
        """
        Setter method for a calendar year. Validates for a correct year.
        Sets attribute year
        :param self: Expects instance of class Calendar
        :param year: Input year provided by user
        :type self: object
        :type year: str
        """
        if not re.search(self.YEAR_REGEX, year, re.IGNORECASE):
            raise ValueError("Invalid Year")
        self._year = year

    @property
    def daysmonth(self: object) -> int:
        """
        Getter method for custom days in a month
        Gets attribute daysmonth of instance.
        :param self: Expects instance of class Calendar
        :type self: object
        :return: (Custom) days in a month
        :rtype: int
        """
        return self._daysmonth

    @daysmonth.setter
    def daysmonth(self: object, daysmonth: int):
        """
        Setter method for custom days in a month. Validats for a correct amount of custom days.
        Sets attribute daysmonth
        :param self: Expects instance of class Calendar
        :param daysmonth: Input daysmonth provided by user
        :type self: object
        :type daysmonth: int
        """
        tDays = get_days_month(self.year, self.month)
        if tDays < int(daysmonth):
            raise ValueError("More days than the month has!")
        self._daysmonth = int(daysmonth)

    def get_valid_input(self: object, prompt: str, setter_attr: str) -> str:
        """
        Validate user input during calendar creation.
        Calls on setters to run validation logic.
        :param self: Expects instance of class Calendar
        :param prompt: Input provided by user
        :type self: object
        :type prompt: str
        :return: The validate user input
        :rtype: str
        """
        while True:
            # Repeat if not valid
            try:
                user_input = input(prompt)
                # Use setattr to assign values to the coresponding class attributes, therefore triggering the setter logic checks in a modular fashion
                setattr(self, setter_attr, user_input)
                return user_input
            except ValueError as e:
                print(e)

    def get_data_for_day(self: object, day: int) -> str:
        """
        Prints out data for a selected day. If there is no data, error will be printed.
        :param self: Expects instance of class Calendar
        :param day: Data to display data from
        :type self: object
        :type day: int
        :return: For validation purposes: the data in said day
        :rtype: str
        """
        day = str(day)  # Ensuring the key is in the correct format
        if day in self.calendar_data:
            data = self.calendar_data[day]
            if data != [""]:
                print(f"Data for day {day} in calendar {self.name}: {', '.join(data)}")
                return f"{', '.join(data)}"
            else:
                print(f"No data found for day {day}")
                return f"No data found for day {day}"
        else:
            print(f"No data stored for day {day}")

    def generate_month_table(self: object):
        """
        An instanced method to generate a tabulated list of days, which form a calendar.
        If there is data in a day, an ! mark will be displayed to signify that.
        Sets custom days if needed, otherwise defaults to days in a month.
        Calculates on whick weekday the 1st day of the month happens.
        :param self: Expects instance of class Calendar
        :type self: object
        """
        # Create a table header
        header = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        # If daysmonth is not set (user chose the default), use the number of days in the month
        if not self.daysmonth:
            num_days = get_days_month(self.year, self.month)
        else:
            num_days = int(self.daysmonth)

        # Calculate the day of the week for the 1st day of the month
        first_day = datetime.datetime(
            int(self.year), datetime.datetime.strptime(self.month, "%B").month, 1
        ).weekday()

        # Initialize the table with empty cells for the days before the 1st day
        calendar_table = [["" for _ in range(7)]]
        current_row = calendar_table[0]

        # Fill in the table with day numbers
        for day in range(1, num_days + 1):
            # Format day with data indicator if data exists and is meaningful for that day
            day_str = str(day)
            day_data = self.calendar_data.get(day_str, [])
            if day_data and any(item.strip() for item in day_data):
                day_display = f"{day}!"
            else:
                day_display = str(day)

            current_row[(day + first_day) % 7] = day_display

            if (day + first_day) % 7 == 6:
                calendar_table.append(["" for _ in range(7)])
                current_row = calendar_table[-1]

        # Print the table using tabulate
        print(f"\n****'!' marks days that contain data****")
        print(f"Calendar '{self.name}' for {self.month}, {self.year}")
        print(tabulate(calendar_table, headers=header, tablefmt="fancy_grid"))

    def add_data_to_day(self: object, day: int, data: str):
        """
        An instanced method to add data of given day in a calendar.
        Validates for valid input.
        :param self: Expects instance of class Calendar
        :param day: Day to add data to
        :param data: Data to add to day
        :type self: object
        :type day: int
        :type data: str
        """
        if day < 1 or day > self.daysmonth:
            raise ValueError("Invalid day")

        if day not in self.calendar_data:
            self.calendar_data[str(day)] = []

        self.calendar_data[str(day)].append(data)

    def save_to_json(self: object):
        """
        An instanced method to save calendar data to json (data.json).
        Validates if there is an entry to update, otherwise appends.
        :param self: Expects instance of class Calendar
        :type self: object
        """
        path = "data.json"
        updated = False

        all_calendars = []

        try:
            with jsonlines.open(path, mode="r") as reader:
                for calendar in reader:
                    if calendar["name"] == self.name:
                        # Update the existing calendar with the current instance's data
                        all_calendars.append(self.__dict__)
                        updated = True
                    else:
                        all_calendars.append(calendar)
        except FileNotFoundError:
            pass

        if not updated:
            all_calendars.append(self.__dict__)

        with jsonlines.open(path, mode="w") as writer:
            writer.write_all(all_calendars)

    def edit_data_for_day(self: object):
        """
        An instanced method to edit data of defined day of a loaded calendar.
        Validates for valid input, otherwise reprompts.
        Saves the new data to data.json
        :param self: Expects instance of class Calendar
        :type self: object
        :return: Data of calendar
        :rtype: dict
        """
        while True:
            try:
                day_select = int(input("Data of which day to edit? "))
                if day_select < 1 or day_select > self._daysmonth:
                    raise ValueError("Invalid day")
                new_data = input("New data: ")
                self.calendar_data[str(day_select)] = [
                    new_data
                ]  # Ensure we update the correct key
                break
            except ValueError:
                print("Please enter a valid int value")
                pass

        # Save the changes to the JSON file
        self.save_to_json()

        return self.calendar_data

    def enter_data(self: object, daysmonth: int):
        """
        A function to add data during calendar creation. Adapts to custom days, if given.
        :param calendar: An object of Calendar
        :param daysmonth: Custom Days / Amount of days in a month
        :type calendar: object
        :type daysmonth: int
        """
        self.daysmonth = daysmonth
        for day in range(1, int(daysmonth) + 1):
            data = input(f"Enter data for day {day}: ")
            self.add_data_to_day(day, data)
        self.generate_month_table()

    @staticmethod
    def delete_calendar(name: str):
        with open("data.json", "r") as f:
            lines = f.readlines()

        with open("data.json", "w") as f:
            for line in lines:
                if not line.startswith('{"name": "' + name + '"'):
                    f.write(line)


class Menu:
    OPTION_QUIT = "q"

    def __init__(self: object, header: str, options: list, instructions: str):
        """
        An instanced method to initialize class Menu
        :param self: Expects instance of class Menu
        :param header: Heading of the menu. Can be printed on demand using instanced method get_header vor class Menu.
        :param options: Available options in the generated menu.
        :type self: object
        :type header: str
        :type options: list containing str
        :type instructions: str
        """
        self.options = options
        self.header = header
        self.options_count = len(options)
        self.instructions = instructions

    def display_menu(self: object):
        """
        An instanced method to print a menu.
        :param self: Expects instance of class Menu
        :type self: object
        """
        print(self.instructions)
        table = [[index, option] for index, option in enumerate(self.options, start=1)]
        print(tabulate(table, headers=["Option", "Action"], tablefmt="fancy_grid"))

    def get_selection(self: object) -> int:
        """
        An instanced method to get the user's menu selection. Validates if a correct value has been provided.
        Otherwise reprompts.
        :param self: Expects instance of class Menu
        :type self: object
        :return: Selected option
        :rtype: int
        """
        while True:
            try:
                user_input = input("Enter number: ")
                selected_option = int(user_input)
                if 0 < selected_option <= self.options_count:
                    if selected_option == 4:
                        if self.header == "Save":
                            return 4
                        else:
                            return Menu.OPTION_QUIT
                else:
                    raise ValueError
                return selected_option
            except ValueError:
                self.display_menu()
                pass

    def get_header(self):
        print(pyfiglet.figlet_format(self.header))


def main():
    """
    Acts as the entry point for the program and controls the flow of the application.
    It provides a menu-driven interface for the user to interact with the calendar objects.
    """
    menu = create_menu(
        "AdCalendar",
        [
            "Create a new calendar",
            "Load an existing calendar",
            "Delete a calendar",
            "Quit",
        ],
    )
    menu.get_header()
    while True:
        menu.display_menu()
        user_input = menu.get_selection()
        if user_input == 1:
            create_new_calendar()
        elif user_input == 2:
            adCalendar = print_available_calendars()
            save_menu = create_menu(
                "Save", ["Read entry", "Edit entry", "Back to main menu"]
            )
            while True:
                save_menu.display_menu()
                user_input_dialogue = save_menu.get_selection()
                if user_input_dialogue == 1:
                    user_day = input(
                        "For which day do you want to read the data? Enter number: "
                    )
                    adCalendar.get_data_for_day(int(user_day))
                elif user_input_dialogue == 2:
                    day_data = adCalendar.edit_data_for_day()
                    adCalendar.calendar_data = day_data
                    read_json("y", adCalendar.name)
                elif user_input_dialogue == 3:
                    break
        elif user_input == 3:
            adCalendar = print_available_calendars(True)
            Calendar.delete_calendar(adCalendar.name)
        elif user_input == Menu.OPTION_QUIT:
            sys.exit("Exit Application")


def is_calendar_name_unique(name: str) -> bool:
    """
    A static method to check if the calendar name inputs is unique (from data.json).
    Validates for valid input, otherwise reprompts.
    :param name: A name for a calendar
    :type name: str
    :return: Name is unique
    :rtype: bool
    """
    try:
        with open("data.json", "r") as file:
            for line in file:
                calendar = json.loads(line)
                if calendar["name"] == name:
                    return False
    except FileNotFoundError:
        pass  # If the file does not exist, the name is considered unique
    return True


def create_menu(header: str, options=[]) -> object:
    """
    A function to create tabulated menus with desired menu items. Constructcs object of class Menu.
    :param header: Heading of the menu. Can be printed on demand using instanced method get_header vor class Menu.
    :param options: Available options in the generated menu.
    :type options: list containing str
    :type header: str
    :return: Instanced object of class Menu
    :rtype: 'Menu' object
    """
    return Menu(
        header,
        options,
        "****Choose an option!****",
    )


def create_new_calendar():
    """
    A function to create a new calendar. Constructcs object of classes Calendar and Menu.
    Saves calendar to json (data.json)
    """
    adCalendar = Calendar()
    get_calendar_input(adCalendar)
    save_menu = create_menu("Save", ["Save calendar"])
    save_menu.display_menu()
    user_input_save = save_menu.get_selection()

    if user_input_save == 1:
        adCalendar.save_to_json()


def print_available_calendars(delete=False) -> object:
    """
    A function to print saved calendars.
    Gets data from json (data.json)read_json
    """
    print("***Available calendars***")
    adCalendar = read_json(delete=delete)
    return adCalendar


def read_json(silent="n", selector="", delete=False):
    """
    A function to read stored data in json (data.json). Costructs object of class Calendar when loading stored calendar.
    Prints available calendars as well.
    :param silent: Flag to avoid printing available calendars.
    :param selector: Name of a given calendar.
    :type silent: str
    :type selector: str
    :return: a Calendar object or None
    :rtype: Object or None
    """
    if delete == True:
        action_selector = "Which calendar do you want to delete? Enter calendar name: "
    else:
        action_selector = "Which calendar do you want to load? Enter calendar Name: "

    calendar_data = {}
    while True:
        try:
            with open("data.json", "r") as file:
                for line in file:
                    calendar = json.loads(line)
                    calendar_data[calendar["name"]] = calendar

            if silent != "y":
                print("***Available calendars***")
                calendar_data_list = [
                    (index, name) for index, name in enumerate(calendar_data, start=1)
                ]
                table = tabulate(
                    calendar_data_list,
                    headers=["Index", "Calendar Name"],
                    tablefmt="fancy_grid",
                )
                print(table)

                selector = input(action_selector)

            selected_calendar = calendar_data.get(selector)
            if selected_calendar != None:
                adCalendar = Calendar(
                    selected_calendar["name"],
                    selected_calendar["_month"],
                    selected_calendar["_year"],
                    selected_calendar["_daysmonth"],
                    selected_calendar["days"],
                    selected_calendar["calendar_data"],
                )
                if delete is not True:
                    adCalendar.generate_month_table()
                return adCalendar
            else:
                print(f"Calendar '{selector}' does not exist.")
                pass
        except FileNotFoundError:
            print("File 'data.json' not found.")
            return None


def get_calendar_name(adCalendar):
    while True:
        adCalendar.name = input("What do you want to call this calendar? ")
        if not is_calendar_name_unique(adCalendar.name):
            print(
                f"A calendar with the name '{adCalendar.name}' already exists. Please choose a different name."
            )
        else:
            return adCalendar.name


def get_calendar_year_and_month(adCalendar):
    year = adCalendar.get_valid_input(
        "For which year do you want to generate a calendar? ", "year"
    )
    month = adCalendar.get_valid_input(
        "For which month do you want to generate a calendar? ", "month"
    )
    return year, month


def get_calendar_days(year, month, adCalendar):
    cal_custom_day_selector = f"Do you want to use the default amount of days for this month ({get_days_month(year, month)}) [Y/n]? "
    while True:
        use_default_input = input(cal_custom_day_selector).lower()
        if re.match(r"^[yn]$", use_default_input):
            use_default = use_default_input
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

    if use_default == "n":
        daysmonth = adCalendar.get_valid_input(
            f"For how many days do you want to run the calendar in {month}? ",
            "daysmonth",
        )
        adCalendar.enter_data(int(daysmonth))
    else:
        adCalendar.enter_data(get_days_month(year, month))


def get_calendar_input(adCalendar: object):
    """
    Gets user input to create a new calendar. Validates given input.
    Reprompts if needed.
    :param adCalendar: a Calendar
    :type adCalendar: object
    """
    get_calendar_name(adCalendar)
    year, month = get_calendar_year_and_month(adCalendar)
    get_calendar_days(year, month, adCalendar)


def get_days_month(year: str, month: str) -> int:
    """
    A function to get the amount of days in a month. Accounts for leap years and such.
    :param year: A given year
    :param month: A given month
    :type year: str
    :type month: str
    :return: Amount of days in a given month
    :rtype: int
    """
    date_format = "%B"
    dateObject = datetime.datetime.strptime(month, date_format)
    dmonth = calendar.monthrange(int(year), dateObject.month)[1]
    return dmonth


if __name__ == "__main__":
    main()
