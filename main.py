"""
This is the main module of an Appointment Management System. It provides an interactive command-line interface for managing users and their appointments.

The system allows the user:
    -Add new user
    -Delete an existing user
    -List existing users
    -Schedule an appointment
    -Cancel an appointment
    -reschedule
    -Check for appointment on certain date and time
    -Retrieve purpose of an appointment
"""

from data.User import User
from data.AppointmentDiary import AppointmentDiary
from utils.dbHandler import dbHandler

# connect database
import os
from dotenv import load_dotenv
load_dotenv()
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")

db_handler = dbHandler(db_name, db_user, db_pass, db_host, db_port)

def exit_program():
    print('\nGoodbye!\n')
    exit()

if __name__ == '__main__':
    # map the user's choice to the appropriate method
    options = {'a': User(db_handler).add_user,'d': User(db_handler).delete_user, 'l': User(db_handler).show_users,'s': AppointmentDiary(db_handler).schedule_appt,'c': AppointmentDiary(db_handler).cancel_appt, 'f': AppointmentDiary(db_handler).get_appt_info,'p': AppointmentDiary(db_handler).get_appt_purpose,'r':AppointmentDiary(db_handler).reschedule_appt,'x': exit_program}
    # terminate only if user choose to exit
    while True:
        print('\nWelcome to Appointment Management System! What would you like to do?\n'+'\n'+'[a] Add new user'+'\n'+'[d] Delete an existing user'+'\n'+'[l] List existing users'+'\n'+'[s] Schedule an appointment'+'\n'+'[c] Cancel an appointment'+'\n'+'[f] Check for appointment on certain date and time'+'\n'+'[p] Retrieve purpose of an appointment'+'\n'+'[r] Reschedule an existing appointment'+'\n'+'[x] Exit the system')
        try:
            # prompt user for choice
            choice = input('\nEnter Choice: ').lower()
            if choice in ['a', 'd', 'l', 'x', 's', 'c', 'f', 'p', 'r']:
                print('\n',options[choice]())
            elif choice == 'admin': # for checking purpose
                print(db_handler.get_all())
            else:
                print('Please enter a/d/l/s/c/f/p/r/x.')
        except ValueError:
            print('Please enter a/d/l/s/c/f/p/r/x.')