import sys
import os

# Get the absolute path of the 'main dir' directory
main_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add 'main dir' to the Python path
sys.path.append(main_dir_path)

# Now you should be able to import 'DatabaseHandler' from 'util' package
from util.DatabaseHandler import DatabaseHandler

class User:
    """A class that represents a user in the appointment management system.
    Attributes:
        name (str): The name of the user.
        appointment_diary (AppointmentDiary()): The appointment diary of the user.
    """

    def __init__(self, db_handler) -> None:
        """Initializes a new User instance.
        Args:
            name (str): The name of the user.
        """
        self.db_handler = db_handler

    def add_user(self) -> str:
        username = User.validate_username()
        query = "INSERT INTO appointment_system.users (username) VALUES (%s);"
        if self.db_handler.execute_query(query, username):
            return "User added successfully."
        else:
            return "Error adding user."
    
    def delete_user(self) -> str:
        username = User.validate_username()
        # check if exist
        if not self.get_user_id_by_username(username):
            return "User not found. Please enter a valid username."
        # if found
        query = "DELETE FROM appointment_system.users WHERE username = %s;"
        if self.db_handler.execute_query(query, username):
            return "User deleted successfully."
        else:
            return "Error deleting user."
    
    def check_user(self) -> bool:
        username = User.validate_username()
        query = "SELECT username FROM appointment_system.users WHERE username = %s;"
        return self.db_handler.fetch_one(query, username) is not None
    
    def show_users(self) -> list:
        query = "SELECT username FROM appointment_system.users;"
        users = self.db_handler.fetch_all(query)
        return [user[0] for user in users]
    
    def find_user_id(self):
        username = User.validate_username()
        return self.get_user_id_by_username(username)
    
    def get_user_id_by_username(self, username: str):
        """
        Retrieve the user_id based on the provided username.
        Args:
            username (str): The username of the user.
        Returns:
            Optional[int]: The user_id if the user exists, or None if the user is not found.
        """
        query = "SELECT user_id FROM appointment_system.users WHERE username = %s;"
        result = self.db_handler.fetch_one(query, username)
        if result:
            return result[0]
        return None
    
    @staticmethod
    def validate_username():
        while True:
            username = input("\nEnter your username: ")

            if len(username) < 2:
                print("Username must be at least 2 characters long.")
            elif not username.isalnum() or not any(c.isalpha() for c in username):
                print("Username can only contain letters and numbers. Please try again.")
            elif username[0] in '-_':
                print("Username cannot start with a hyphen or underscore. Please try again.")
            elif username[-1] in '-_':
                print("Username cannot end with a hyphen or underscore. Please try again.")
            elif '--' in username or '__' in username:
                print("Username cannot have consecutive hyphens or underscores. Please try again.")
            else:
                return username


if __name__ == '__main__':
    pass
    # db_handler = DatabaseHandler("appt_sys_db", "huiruy", "0000", "localhost", "5432")
    # user = User(db_handler)

    # Now you can use the user object to perform user-related operations.
    # For example:
    # username = "john_doe"
    # user.add_user()    # Add a new user
    # print(user.delete_user(username))  # Delete a user
    # print(user.check_user("username"))   # Check if a user exists
    # print(user.show_users())           # Show all users