# Easy Scheduler
![alt text](/media/easy-scheduler.png)
Easy Scheduler is a scheduler app with a user-friendly Graphical User Interface (GUI), built with **Python** and **Tkinter**. The app is designed to be simple and intuitive, with a clean and minimalistic interface. Users can effortlessly create, view, update, and delete events, making event management. The application is following the **CRUD** (Create, Read, Update, Delete) paradigm, using a SQLite database to enable persistent storage of appointments. Finally, the app is **executable** on Windows, Linux, and MacOS, making it cross-platform friendly.

To learn more about the application [here](https://www.huiruyang.works/projects/curd-easy-scheduler)

## Table of Contents
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Database](#database)
- [Usage](#usage)

## Key Features
- **Add Event**: Add Event with a title, description, date, and time.
- **View all**: View all events.
- **Search**: Search for events by different criteria.
- **Update Event**: Update an event.
- **Delete Event**Delete an event or all events.

## Technologies Used
- **Python**: Python is the primary programming language used for developing the application, known for its simplicity, readability, and rich standard library.
- **Tkinter**: Tkinter is used to create the GUI, simplifying the process of creating a cross-platform GUI.
- **SQLite**: Base on the current scale of the project, SQLite is the ideal choice for the database, facilitating data storage and retrieval efficiently within the application. 
- **PyInstaller**: PyInstaller is utilized to package the Python application into a standalone executable, ensuring ease of distribution without external Python dependencies.

## Database
The application uses a SQLite database to store appointments. When the application is running, the application will build connection and execute query using the `db_handler.py` file. The databse has a table `event`, it is defined as follows:

| id    | year             | month            | date             | start_time    | end_time      | event_detai   |
|-------|------------------|------------------|------------------|---------------|---------------|---------------|
| 123.. | INTEGER NOT NULL | INTEGER NOT NULL | INTEGER NOT NULL | TEXT NOT NULL | TEXT NOT NULL | TEXT NOT NULL |
| 123.. | ...              | ...              | ...              | ...           | ...           | ...           |
| 123.. | ...              | ...              | ...              | ...           | ...           | ...           |

# Usage
- **Clone the repository**: `git clone`
- **Install dependencies**: `pip install -r requirements.txt`
- **Run the application**: `python main.py`
- **Packaging the application**: `pyinstaller --onefile --windowed main.py`

# Usage (Executable)
- **Download the executable**: link to be added
- **Run the application**: `EasyScheduler.exe`
- **Database**: The database is located in the same directory as the executable, named `events.db`.