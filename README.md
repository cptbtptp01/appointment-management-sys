# Appointment Scheduler
Easy Scheduler is a scheduler app with a user-friendly Graphical User Interface (GUI), built with **Python** and **Tkinter**. The app is designed to be simple and intuitive, with a clean and minimalistic interface. Users can effortlessly create, view, update, and delete appointments, making appointment management. The application is following the **CRUD** (Create, Read, Update, Delete) paradigm, using a SQLite database to enable persistent storage of appointments.

## Functionality
1. Schedule appointment for a certain date, time interval (indicated by start time and end time), and purpose if no conflicts found.
2. Cancel the appointment for a specified date and time interval.
3. Check whether user has an appointment during a given time interval on a date.
4. Retrieve the purpose of an appointment at a given date, time interval.
5. Reschedule an existing appointment to a new date or time if no conflicts found.

## Usage
To run the program, simply execute the main.py file. This will launch the interactive command-line interface, which allows you to manage users and their appointments. Follow the prompts to select an option from the main menu, and provide any necessary additional information.

## About the program

A command line tool, has the following functions:

    	-Add new user
    	-Delete an existing user
    	-List existing users
    	-Schedule an appointment
    	-Cancel an appointment
    	-reschedule
    	-Check for appointment on certain date and time
    	-Retrieve purpose of an appointment

## Current Structure

### Main class
serve as an entry point, allow user to choose task from the menu

### User class

    A class that represents a user in the appointment management system.
    Attributes:
        name (str): The name of the user.
        appointment_diary (AppointmentDiary()): The appointment diary of the user.
        all_users (dict): {"user1": User object,"user2": User object,"user3": User object, ...}

- __class methods__:
	+ __get_user__:
		Class method that gets a User instance from user input.
        Returns: User instance: an existing user instance or a new user instance
    + __sort_user__:
    	Helper method 
    	Sort all_user dictionary
        Returns: dict (sorted)
    + __add_user__:
    	Class method that adds a new User instance to the system.
        Returns: str: A message indicating whether the user was added or not.
    + __check_user__:
    	Class method that checks if a User instance exists in the system.
        Returns: User or None: A User instance if it exists, None otherwise.
    + __delete_user__:
    	Class method that deletes a User instance from the system.
        Returns: str: A message indicating whether the user was deleted or not.
    + __show_user__:
    	Class method that returns a string contains all usernames in the system.
        Returns: str: A string contains all usernames in the system.
    + __get_all__: (for admin use)
    	Class method that returns a string with information about all user in the system.
        Returns: str: A string with information about all user in the system.

### Appointment class

	A class represents an appointment with a date, start time, end time, and purpose.
    	Attributes:
        	date (Date): The date of the appointment.
        	start_time (Time): The start time of the appointment.
        	end_time (Time): The end time of the appointment.
        	purpose (str): The purpose of the appointment.

- __methods__:
	+ check_conflict(self, other:'Appointment') -> bool
		Checks whether the current Appointment instance conflicts with another Appointment instance.
        Args:
            other (Appointment): The other Appointment instance to check for conflicts.
        Returns: bool: True if there is a conflict, False otherwise.
- __class method__: three getters, create an appointment by taking different arguments.
	+ __get_appt__(cls, date: Date) -> 'Appointment'
		Creates a new Appointment instance by prompting the user for start time, end time, and purpose.
        Args: 
        	date (Date): The date of the appointment.
        Returns: Appointment: The new Appointment instance.
    + __get_appt2__(cls, date: Date, purpose:str) -> 'Appointment'
    	Creates a new Appointment instance by prompting the user for start time and end time.
        Args: 
        	date (Date): The date of the appointment.
            purpose (str): The purpose of the appointment.
        Returns: Appointment: The new Appointment instance.
    + __get_appt3__(cls, date: Date, start_time: Time, end_time: Time) -> 'Appointment'
    	Creates a new Appointment instance by prompting the user for purpose.
        Args:
            date (Date): The date of the appointment.
            start_time (Time): The start time of the appointment.
            end_time (Time): The end time of the appointment.
        Returns:
            Appointment: The new Appointment instance.

### Appointment Diary class
	A class that represents an appointment diary.
    Attributes:
    diary (dict): A dictionary containing dates as keys and a list of appointments for that date as values.

- __methods__:
	+ __sort_diary__
		Helper method Sort diary by the date and appointments by start time.
        Returns:
            dict (sorted)
    + __get_existing__
    	Helper method Checks if current date and time has an appointment.
        Returns:
            list(2 element): 
                -If there is: [date object, appointment object]
                -If date has appointments but no conflict: [date object, time object]
                -If date has no appointment: [message, date object]
    + __get_appt__
    	Prompts the user to retrieving an appointment purpose.
        Pre-condition:
            any time between the start time and end time of the scheduled appointment is allowed for checking
        Returns:
            str: represent a corresponding message to user notifying:
                -If found successfully, with the purpose of the appointment
                -If no appointment found 
    + __schedule_appt__ 
    	Prompts the user to schedule an appointment.
        (ask date -> if date exists -> ask start time & end time -> if not conflict -> ask purpose -> store.)
        Returns:
            str: represent a corresponding message to user notifying:
                -If scheduled successfully
                -If conflicts with existing appointment
    + __cancel_appt__
    	Prompts the user to cancel an appointment.
        Returns:
            str: represent a corresponding message to user notifying:
                -If cancelled successfully
                -If no appointment found
    + __reschedule_appt__
    	Prompts the user to rescheduling an appointment.
        Pre-condition:
            any time between the start time and end time of the scheduled appointment is allowed for checking
        Returns:
            str: represent a corresponding message to user notifying:
                -If rescheduled successfully
                -If no appointment found                
    + __check_appt__
    	Prompts the user to checking an appointment.
        Pre-condition:
            any time between the start time and end time of the scheduled appointment is allowed for checking
        Returns:
            str: represent a corresponding message to user notifying:
                -If found successfully
                -If no appointment found 


## Current Limitation
The information are saved in memory, which means each time exit the program, the info will not exist when run the program the next time.

## Start Refactoring
Goal: Instead of using dictionaries that save info in memory. Use postgreSQL, design a database.

### Set Up Database
#### Create Schema
> A schema is like a container that holds related tables and provides a way to separate and organize different sets of data. In PostgreSQL, you typically organize tables within a schema.

For the appointment system, a single schema is good to go, which can hold both the user and appointment tables.

#### Create User Table
| user_id | username    |
|---------|-------------|
| 123..   | sampleuser1 |
| 345..   | sampleuser2 |
| 456..   | sampleuser3 |

*__user_id__: a `SERIAL` type, which means it will auto-generate a unique integer value for each new user added to the table. It is also the primary key of the table.
__username__: defined as `VARCHAR(100)` and marked as `NOT NULL` to ensure each user has a valid username.*

#### Create Appointment Table
| id | username | date       | start_time | end_time | purpose |
|----------------|---------|------------|------------|----------|---------|
| 123..          | 123..   | YYYY-MM-DD | 9 AM       | 11 AM    | ...     |
| 123..          | 345..   | YYYY-MM-DD | 10 AM      | 11 AM    | ...     |
| 123..          | 456..   | YYYY-MM-DD | 9 AM       | 11 AM    | ...     |

*__id__: a `SERIAL` type, serves as the primary key
__username__: text, represent username, and username need to be not null, unique
__date__: represent the appointment's date
__start_time__: represent the appointment's start time
__end_time__: represent the appointment's end time
__purpose__: represent the appointment's purpose*

# Create User Table > id + username + date + start_time + end_time + purpose
# c.execute("""CREATE TABLE user (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL UNIQUE,
#             date TEXT NOT NULL,
#             start_time TEXT NOT NULL,
#             end_time TEXT NOT NULL,
#             purpose TEXT
# )
# """)

#### TODO GUI
# entries
username = tkinter.Entry(root, width=30)
username.grid(row=0, column=1, padx=20)

date = tkinter.Entry(root, width=30)
date.grid(row=1, column=1, padx=20)

start_time = tkinter.Entry(root, width=30)
start_time.grid(row=2, column=1, padx=20)

end_time = tkinter.Entry(root, width=30)
end_time.grid(row=3, column=1, padx=20)

purpose = tkinter.Entry(root, width=30)
purpose.grid(row=4, column=1, padx=20)

# labels
username_label = tkinter.Label(root, text="Username")
username_label.grid(row=0, column=0)

date_label = tkinter.Label(root, text="Date")
date_label.grid(row=1, column=0)

start_time_label = tkinter.Label(root, text="Start Time")
start_time_label.grid(row=2, column=0)

end_time_label = tkinter.Label(root, text="End Time")
end_time_label.grid(row=3, column=0)

purpose_label = tkinter.Label(root, text="Purpose")
purpose_label.grid(row=4, column=0)

# schedule button
# TODO the buttom will invoke backend function from data/AppointmentDiary.py schedule_appt()
schedule_btn = tkinter.Button(root, text="Schedule", command=lambda: add_appointment()) 
schedule_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# loosely use of figma for UI design