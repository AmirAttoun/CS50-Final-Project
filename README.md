# adCalendar

![Language](https://img.shields.io/badge/language-python-blue)

## Video Demo:  
Video Demo:  TBD

Github: https://github.com/AmirAttoun/CS50-Final-Project

## Description:
Welcome to *"AdCalendar"*!

This project was created as the final project for Harvard University's CS50P Introduction 
to Programming with Python.

The general idea for the program is for it to be able to create calendars which can store 
data for individual days. For now, this data comes in the form of text. The calendars are
made persistent by I/O operations. The intial inspiration was to create an "Advent calendar". 
See Topic Concept of an advent calendar for an explanation of the concept.

The program is interactive and user driven.

## Concept of an "advent calendar"
In Europe, there is the concept of an "Advent Calendar" (hence the ad in adCalendar).
Usually used during the pre-Christmas time, kids (and likeminded adults) can buy a physical
calendar that consists of individual "doors" than are supposed to be opened each day from 
the 1st to the 24th (Christmas Eve). Behind each door there is a piece of chocolate, a note
or other little gifts.
Hence the the idea to create calendars with a limited runtime.

## Features

### Creating calendars
The user can create a calendar for a desired year and month. with said days. If 
nothing is entered (empty string), the calendar will treat this as no data.

The user also has the option to create a calendar with a certaing runtime.
During creation of a calendar, uses can input text to be associated 
Example:
    I can create a calendar for February, 2023 with a custom amount of days of 5.
    This will create a calendar for said month which runs from December 1st 
    to December 5h.

As an abstraction of that, users can also this tool as a general calendar and note
taking application. Therefore the default amount of days in a month is also valid.

### Displaying calendars
Once a calendar has been created, the application will output said calendar in a
tabulated form, indicating with an "!" the days, in which data has been stored. 
To read and edit entries, the calendar first has to be saved.

### Storing calendars
After creatig a calendar, the user has the option to save the generated calendar. 
This will write the generate calendar object to data.json. The names of stored 
calendars have to be unique.

### Loading calendars
In the main menu, the user can load up stored calendars.
Those are read and loaded from data.json

### Deleting calendars
In the main menu, the user has the option to delete a calendar.
The calendar will be remove from data.json

### Data actions
Once loaded, the user can read text entries for the chosen days (entries marked 
with an "!" contain data).
Additionally, a user can edit data for the given days. If there is no data in the 
chosen day, the data will be added as well.
Using the edit functionality automatically writes the data back into data.json.

### Future features 
- Storing data like audio, video, images in addition to text
- A GUI
- Better Menuflow

### Optimization
- Refactoring of certain code elements such as:
    - Methods
    - Functions
    - Classes
- Improvements in unit tests

### Learnings
Feature creep is real.\
Milestones are important.\
The intial setup of a project, for example how classes are structured, might not hold up\
the longer a project goes on. \
Avoid the temptation to hardcode "hacks".\
Refactoring takes time. \
Break down problems into little chunks.\
Persistence. Don't give up, even if you feel like the code is not "optimal". \
Live and learn.\

### Contact
Please do not hesitate to contact me if you have questions regarding the project
or any other related subject. Mail me <a href="mailto:amir.attoun@protonmail.ch">here</a>.