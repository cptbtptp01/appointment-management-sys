from modules.User import User
import util.DateTimeHandler as DateTimeHandler

class AppointmentDiary:
    """A class that represents an appointment diary.
    """
    def __init__(self, db_handler) -> None:
        self.db_handler = db_handler
    
    def schedule_appt(self) -> str:
        """
        Prompts the user to schedule an appointment.

        Returns:
            str: represent a corresponding message to user notifying:
                -If scheduled successfully
                -If conflicts with existing appointment
        """
        
        #get user
        user_id = User(self.db_handler).find_user_id()
        if not user_id:
            return "User not found. Please enter a valid username."

        # get date from user
        date = DateTimeHandler.get_date("date")
        
        # get time from user
        time = DateTimeHandler.get_start_and_end_time()
        if time:
            start_time, end_time = time[0], time[1]
        else:
            return "End time must be later than start time."
        
        # check conflicts
        conflicts = self.check_appointment_conflict(user_id, date, start_time, end_time)
        if conflicts:
            return "Appointment conflicts with an existing appointment."
        
        # ask for entering purpose
        purpose = AppointmentDiary.get_purpose()
        
        # add to db
        if self.add_appointment_to_db(user_id, date, start_time, end_time, purpose):
            return "Appointment scheduled successfully."
        else:
            return "Error scheduling appointment"
    
    def cancel_appt(self) -> str:
        """
        Prompts the user to cancel an appointment.
        Returns:
            str: represent a corresponding message to user notifying:
                -If cancelled successfully
                -If no appointment found 
        """
        # Find user id base on user input
        user_id = User(self.db_handler).find_user_id()

        if not user_id:
            return "User not found. Please enter a valid username."
        
        # get date
        date = DateTimeHandler.get_date("date")
        # get time
        start_time = DateTimeHandler.get_time("cancel")
        
        # check if exists
        appt_exists = self.check_appt_start_time(user_id, date, start_time)
        if not appt_exists:
            return "No appointment found for the specified date, and time."
        
        self.delete_appt(user_id, date, start_time)
        return "Appointment cancelled successfully."
    
    def get_appt_purpose(self) -> str:
        """
        Prompts the user to retrieving an appointment purpose.
        Pre-condition:
            any time between the start time and end time of the scheduled appointment is allowed for checking
        Returns:
            str: represent a corresponding message to user notifying:
                -If found successfully, with the purpose of the appointment
                -If no appointment found 
        """
        # Find user id base on user input
        user_id = User(self.db_handler).find_user_id()
        if not user_id:
            return "User not found. Please enter a valid username."
        
        # get date
        date = DateTimeHandler.get_date("date")
        
        # get time
        time = DateTimeHandler.get_time("between")

        # check
        appointment = self.check_appt_time_in_between(user_id, date, time)
        if appointment:
            return f"Purpose: {appointment[5]}"
        else:
            return "No appointment found for the specified date, and time."
    
    def get_appt_info(self) -> str:
        """
        Prompts the user to retrieving an appointment's date, time, purpose.
        Pre-condition:
            any time between the start time and end time of the scheduled appointment is allowed for checking
        Returns:
            str: represent a corresponding message to user notifying:
                -If found successfully, return full information of the appointment
                -If no appointment found 
        """
        # Find user id base on user input
        user_id = User(self.db_handler).find_user_id()

        if not user_id:
            return "User not found. Please enter a valid username."
        
        # get date
        date = DateTimeHandler.get_date("date")
        
        # get time
        time = DateTimeHandler.get_time("between")

        # check
        appointment = self.check_appt_time_in_between(user_id, date, time)
        if appointment:
            return f'Date: {appointment[2]}, Start Time: {appointment[3]}, End Time: {appointment[4]}, Purpose: {appointment[5]}'
        else:
            return "No appointment found for the specified date, and time."
    
    def reschedule_appt(self) -> str:
        """
        Prompts the user to rescheduling an appointment.
        Pre-condition:
            any time between the start time and end time of the scheduled appointment is allowed for checking
        Returns:
            str: represent a corresponding message to user notifying:
                -If rescheduled successfully
                -If no appointment found 
        """
        
        # Find user id base on user input
        user_id = User(self.db_handler).find_user_id()
        if not user_id:
            return "User not found. Please enter a valid username."
        
        # get date
        date = DateTimeHandler.get_date("date")
        
        # get time
        input = "between"
        given_time = DateTimeHandler.get_time(input)

        # check
        appointment = self.check_appt_time_in_between(user_id, date, given_time)
        if not appointment:
            return "No appointment found for the specified date, and time."
        
        # if found, save purpose in temp variable & delete current first
        old_start_time = appointment[3]
        purpose = appointment[5]
        self.delete_appt(user_id, date, old_start_time)

        # ask for new start time and end time
        new_date = DateTimeHandler.get_date("new_date")
        new_time = DateTimeHandler.get_start_and_end_time()   
        # check conflicts
        if self.check_appointment_conflict(user_id, new_date, new_time[0], new_time[1]):
            return "Appointment conflicts with an existing appointment."
        else:
            self.add_appointment_to_db(user_id, new_date, new_time[0], new_time[1], purpose)
            return "Appointment rescheduled successfully."

    def add_appointment_to_db(self, user_id, date, start_time, end_time, purpose) -> bool:
        """
        Helper
        add appointment to db
        """
        query_schedule = "INSERT INTO appointment_system.appointments (user_id, date, start_time, end_time, purpose) VALUES (%s, %s, %s, %s, %s);"
        return self.db_handler.execute_query(query_schedule, user_id, date, start_time, end_time, purpose)
    
    def check_appt_start_time(self, user_id, date, start_time):
        """
        Helper
        checking an appointment with start time.
        Pre-condition:
            time equals start time
        Returns:
            the appointment if found, none otherwise  
        """
        query_check_appointment = "SELECT * FROM appointment_system.appointments WHERE user_id = %s AND date = %s AND start_time = %s;"
        
        return self.db_handler.fetch_one(query_check_appointment, user_id, date, start_time)
    
    def check_appt_time_in_between(self, user_id, date, given_time):
        """
        Helper
        checking an appointment with given time.
        Pre-condition:
            any time between the start time and end time of the scheduled appointment is allowed for checking
        Returns:
            the appointment if found, none otherwise 
        """
        query = """
            SELECT * FROM appointment_system.appointments
            WHERE user_id = %s AND date = %s AND %s BETWEEN start_time AND end_time;
        """
        return self.db_handler.fetch_one(query,user_id, date, given_time)
        
    
    def delete_appt(self, user_id, date, start_time) -> None:
        """
        Helper
        delete appointment in db
        """
        query_cancel_appt = "DELETE FROM appointment_system.appointments WHERE user_id = %s AND date = %s AND start_time = %s;"
        self.db_handler.execute_query(query_cancel_appt, user_id, date, start_time)
    
    def check_appointment_conflict(self, user_id, date, start_time, end_time):
        """
        Helper
        Check for appointment conflicts for the specified user, date, and time.
        Args:
            user_id (int): The user_id for which to check for conflicts.
            date (date): The date of the appointment (format: "YYYY-MM-DD").
            start_time (str): The start time of the appointment (format: "HH:MM").
            end_time (str): The end time of the appointment (format: "HH:MM").

        Returns:
            bool: True if there is a conflict, False otherwise.
        """
        query_conflict = "SELECT * FROM appointment_system.appointments WHERE user_id = %s AND date = %s AND ((start_time <= %s AND end_time > %s) OR (start_time < %s AND end_time >= %s) OR (start_time >= %s AND end_time <= %s));"
        conflicts = self.db_handler.fetch_all(query_conflict, user_id, date, start_time, start_time, end_time, end_time, start_time, end_time)
        return bool(conflicts)
    
    @staticmethod
    def get_purpose() -> str:
        """
        Prompting the user for purpose.
        Returns:
            str: The new Appointment instance.
        """
        while True:
            try:   
                purpose = input("Enter your purpose:")
                if purpose:
                    return purpose
            except ValueError:
                print('Please enter valid purpose.')