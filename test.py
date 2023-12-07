#delete an entry
#{"name": "NEWSD", "_month": "December", "_year": "2023", "days": 0, "_daysmonth": 4, "calendar_data": {"1": ["da"], "2": [""], "3": ["ta"], "4": [""]}}
#{"name": "asdfasdfasfd", "_month": "December", "_year": "2023", "days": 0, "_daysmonth": 2, "calendar_data": {"1": ["data"], "2": [""]}}

with open("data.json", "r") as f:
    lines = f.readlines()

with open("data.json", "w") as f:
    for line in lines:
        if not line.startswith('{"name": "asdfasdfasfd"'):
            f.write(line)
