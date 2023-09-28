from datetime import datetime
import calendar
import tkinter as tk
from tkinter import ttk, messagebox

from db.db_handler import DatabaseHandler
from gui.custom_widgets import CustomDropdown, CustomLabel, CustomButton

class EventApp:
    def __init__(self):
        # Creating instance
        self.root = tk.Tk()
        self.root.title("Easy Scheduler")
        self.tk_message_box = messagebox
        self.ttk = ttk
        # Connecting to database
        self.db_handler = DatabaseHandler('./db/appointments.db')

        # Initializing functions
        self.root.resizable(0, 0)
        self.create_menu()
        self.create_navigation_tabs()
        self.add_event_tab()
        self.retrieve_event_tab()
        self.delete_event_tab()

    def on_click_create(self):
        """Adding the event in the database"""
        # get the values from the dropdowns
        values = self._get_dropdown_values()
        event_detail = self.event_detail.get("1.0", tk.END)
        year, month_num, day, start_time, end_time = values
        if not self.db_handler.is_valid_event(year, month_num, day, start_time, end_time, event_detail):
            self.tk_message_box.showerror("Invalid Event", "Please enter valid event details")
            return
        
        self.db_handler.add_event(year, month_num, day, start_time, end_time, event_detail)
        self.tk_message_box.showinfo("Success", "Event added successfully")
        self.event_detail.delete("1.0", tk.END)
    
    def on_click_all_event(self):
        """Getting all the events from the database"""
        events = self.db_handler.get_all_events()
        if not events:
            self.tk_message_box.showinfo("No Events", "No events found")
            return
        for event in events:
            self.all_events_box.insert(tk.END, self._format_event(event))

    def on_click_clear(self):
        """Clear all events from the database """
        self.tk_message_box.showinfo("Confirm","Are you sure you want to delete all your events?")
        self.db_handler.clear_all_events()
    
    def on_click_search(self):
        """Searching the event in the database"""
        # clear the listbox
        self.result_box.delete(0, tk.END)
        # get the values from the dropdowns
        values = self._get_dropdown_values()
        year, month_num, day, start_time, end_time = values
        query = "SELECT * FROM appointments WHERE "
        events = self.db_handler.find_event(query, year, month_num, day, start_time, end_time)
        if not events:
            self.tk_message_box.showinfo("No Events", "No events found")
            return
        for event in events:
            self.result_box.insert(tk.END, self._format_event(event))
    
    def on_click_delete(self):
        """Deleting the event from the database"""
        # clear the listbox
        self.result_box.delete(0, tk.END)
        # get the values from the dropdowns
        values = self._get_dropdown_values()
        year, month_num, day, start_time, end_time = values
        query = "SELECT id FROM appointments WHERE "
        event_id = self.db_handler.find_event(query, year, month_num, day, start_time, end_time)
        self.tk_message_box.showinfo("Confirm","Delete will remove all the events from the search result. Are you sure you want to delete?")
        self.db_handler.delete_event(event_id)
        self.result_box.delete(0, tk.END)
    
    def create_menu(self):
        """Creating the menu bar"""
        self.menu_bar = tk.Menu(self.root)
        self.root.configure(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New")
        self.file_menu.add_command(label="Exit", command=self.root.destroy)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self._msg_box)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
    
    def create_navigation_tabs(self):
        """Adding tabs to make navigation
            tabs: 
                - Adding event
                - Retrieving event
                - Deleting event
        """
        self.tab_notebook = ttk.Notebook(self.root)

        self.tab_add_event = ttk.Frame(self.tab_notebook)
        self.tab_retrieve_event = ttk.Frame(self.tab_notebook)
        self.tab_delete_event = ttk.Frame(self.tab_notebook)

        self.tab_notebook.add(self.tab_add_event, text="ADD EVENT")
        self.tab_notebook.add(self.tab_retrieve_event, text="RETRIEVE EVENT")
        self.tab_notebook.add(self.tab_delete_event, text="DELETE EVENT")

        self.tab_notebook.pack(expand=1, pady=5, fill="both")

    def add_event_tab(self):
        """Content of the Add event tab"""
        root1 = ttk.LabelFrame(self.tab_add_event, text="Add Event")
        root1.grid(column=0, row=0, padx=8, pady=4, sticky="W")
        
        self._create_dropdowns(root1)
        
        self.event_label = CustomLabel(root1, "Enter your event details")
        self.event_label.grid(column=0, row=2, padx=8, pady=4, sticky="W")
        self.event_detail = tk.Text(root1, width=50, height=2)
        self.event_detail.grid(column=0, row=3, pady=(10,0), sticky="W")

        self.all_events_box = tk.Listbox(root1, width=50, height=15)
        self.all_events_box.grid(column=0, row=4, pady=(10,0), sticky="W")

        create_button = CustomButton(root1, "CREATE", self.on_click_create)
        create_button.grid(column=0, row=5, pady=(10,0), sticky="W")
        view = CustomButton(root1, "All Events", self.on_click_all_event)
        view.grid(column=0, row=6, pady=(10,0), sticky="W")       

    def retrieve_event_tab(self):
        """Content of the Retrieve event tab"""
        root2 = ttk.LabelFrame(self.tab_retrieve_event, text="Retrieve Event")
        instruction_message = CustomLabel(root2, text="Note: Please select at least one of the following options to retrieve event")
        root2.grid(column=0, row=0, padx=8, pady=4, sticky="W")
        instruction_message.grid(column=0, row=2, padx=8, pady=4, sticky="W")

        self._create_dropdowns(root2)

        self.result_box = tk.Listbox(root2, width=50, height=15)
        self.result_box.grid(column=0, row=4, pady=(10,0), sticky="W")
        search_button = CustomButton(root2, "SEARCH", self.on_click_search)
        search_button.grid(column=0, row=5, pady=(10,0), sticky="W")

    def delete_event_tab(self):
        """Content of the Delete event tab"""
        root3 = ttk.LabelFrame(self.tab_delete_event, text="Delete Event")
        instruction_message1 = CustomLabel(root3, text="Note: Please select at least one of the following options to delete event.")
        instruction_message2 = CustomLabel(root3, text="If you want to delete all events just click on delete all button")
        root3.grid(column=0, row=0, padx=8, pady=4, sticky="W")
        instruction_message1.grid(column=0, row=2, padx=8, pady=4, sticky="W")
        instruction_message2.grid(column=0, row=3, padx=8, pady=4, sticky="W")

        self._create_dropdowns(root3)
        self.result_box = tk.Listbox(root3, width=50, height=15)
        self.result_box.grid(column=0, row=4, pady=(10,0), sticky="W")
        search_button = CustomButton(root3, "SEARCH", self.on_click_search)
        delete_button = CustomButton(root3, "DELETE", self.on_click_delete)
        delete_all_button = CustomButton(root3, "DELETE ALL", self.on_click_clear)
        search_button.grid(column=0, row=5, pady=(10,0), sticky="W")
        delete_button.grid(column=0, row=6, pady=(10,0), sticky="W")
        delete_all_button.grid(column=0, row=7, pady=(10,0), sticky="W")
    
    def run(self):
        """Running the app"""
        self.root.mainloop()
    
    def _format_event(self, event: list) -> str:
        """Formatting the event"""
        _, year, month, day, start_time, end_time, event_detail = event
        return f"{year}-{month:02d}-{day:02d} {start_time}-{end_time} {event_detail}"

    def _get_dropdown_values(self) -> list:
        """Getting the values from the dropdowns"""
        year = self.year_dropdown.get_text()
        month = self.month_dropdown.get_text()
        month_num = list(calendar.month_abbr).index(month)
        day = self.day_dropdown.get_text()
        start_time = self.start_time_dropdown.get_text()
        end_time = self.end_time_dropdown.get_text()
        return [year, month_num, day, start_time, end_time]

    def _create_dropdowns(self, parent_frame):
        """Creating the dropdowns"""
        year_options = [""]
        year_options += [str(year) for year in range(2023, 2030)]
        self.year_dropdown = CustomDropdown(parent_frame, "Year", year_options)
        self.year_dropdown.grid(column=0, row=0, sticky="W")
        month_options = [""]
        month_options += [datetime(1900, month, 1).strftime('%b') for month in range(1, 13)]
        self.month_dropdown = CustomDropdown(parent_frame, "Month", month_options)
        self.month_dropdown.grid(column=1, row=0, sticky="W")
        day_options = [""]
        day_options += [str(day) for day in range(1, 32)]
        self.day_dropdown = CustomDropdown(parent_frame, "Day", day_options)
        self.day_dropdown.grid(column=2, row=0, sticky="W")
        time_options = [""]
        time_options += [f'{hour}:00 AM' if hour <= 12 else f'{hour - 12}:00 PM' for hour in range(1, 25)]
        self.start_time_dropdown = CustomDropdown(parent_frame, "Start Time", time_options)
        self.start_time_dropdown.grid(column=0, row=1, pady=(10,0), sticky="W")
        self.end_time_dropdown = CustomDropdown(parent_frame, "End Time", time_options)
        self.end_time_dropdown.grid(column=1, row=1, pady=(10,0), sticky="W")

    def _msg_box(self):
        """Creating the message box"""
        self.tk_message_box.showinfo(
            'About the App',
            'This App is designed to create a schedule for the days(YYYY-MM-DD)'
            'with an hour between between the times. The schedule can be accessed by the days'
        )

if __name__ == "__main__":
    app = EventApp()
    app.db_handler.create_table()
    app.run()
    app.db_handler.close()