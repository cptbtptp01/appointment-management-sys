import datetime

def get_date(c):
    _input = {"date":"Enter the date (YYYY-MM-DD): ", 
              "new_date": "Enter the new date (YYYY-MM-DD): ",
              }
    while True:
        date_input = input(_input[c])
        try:
            date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            return date
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def get_time(c: str):
    _input = {"cancel":"Enter the start time of the appointment to cancel (HH:MM): ", 
              "between": "Enter the time between start time and end time (HH:MM): ",
              }
    while True:
        time_input = input(_input[c])
        try:
            time = datetime.datetime.strptime(time_input, "%H:%M").time()
            return time
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM format.")

def get_start_and_end_time():
    while True:
        try:
            time_input1 = input("Enter the start time (HH:MM): ")
            start_time = datetime.datetime.strptime(time_input1, "%H:%M").time()

            time_input2 = input("Enter the end time (HH:MM): ")
            end_time = datetime.datetime.strptime(time_input2, "%H:%M").time()

            if end_time > start_time:
                return (start_time, end_time)
            else:
                print("End time should be greater than start time. Please try again.")
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM format.")

if __name__ == '__main__':
    # Test the function
    # time = get_time()
    time = get_start_and_end_time()
    # print("Start time:", time[0])
    # print("End time:", time[1])
