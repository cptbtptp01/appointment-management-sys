import sys
import os

# Get the path to the project root (assuming this script is in the tests directory)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the project root to the Python path
sys.path.insert(0, project_root)
from db.db_handler import DatabaseHandler as db

"""data fields:
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    event_detail TEXT NOT NULL

    example fake data:
    (1, 2021, 1, 1, '12:00 PM', '1:00 PM', 'Lunch with friends')
"""

my_db = db('./db/scheduler.db')

fake_data = [
    [2021, 1, 1, '12:00 PM', '1:00 PM', 'Lunch with friends'],
    [2021, 1, 1, '1:00 PM', '2:00 PM', 'Meeting with boss'],
    [2021, 1, 1, '2:00 PM', '3:00 PM', 'Onboarding'],
    [2022, 2, 2, '9:00 AM', '10:00 AM', 'Team meeting'],
    [2022, 2, 2, '10:00 AM', '11:00 AM', 'Client presentation'],
    [2022, 2, 3, '3:00 PM', '4:00 PM', 'Project planning']
]
print("BEFORE: ",my_db.get_all_events())
for data in fake_data:
    my_db.add_event(*data)

# check all data in db after adding fake data
print("AFTER: ", my_db.get_all_events())
