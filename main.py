from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from db.db_handler import DatabaseHandler
from gui.add_event_tab import AddEventTab
from gui.retrieve_event_tab import RetrieveEventTab
from gui.update_window import UpdateEventWindow
from gui.delete_event_tab import DeleteEventTab

class EventApp:
    def __init__(self):
        # Creating instance
        self.root = tk.Tk()
        self.root.title("Easy Scheduler")
        self.tk_message_box = messagebox
        self.ttk = ttk
        # Connecting to database
        self.db_handler = DatabaseHandler('./db/scheduler.db')

        # Initializing functions
        self.root.resizable(0, 0)
        self._create_navigation_tabs()
        
        # Create instances of other tabs as needed
        self.add_event_tab = AddEventTab(self.tab_add_event, self.on_click_create, self.on_click_all_event, self.on_click_update)
        self.retrieve_event_tab = RetrieveEventTab(self.tab_retrieve_event, self.on_click_search, self.on_click_update)
        self.delete_event_tab = DeleteEventTab(self.tab_delete_event, self.on_click_search_in_delete, self.on_click_delete, self.on_click_delete_all)

    def on_click_create(self):
        """This function is called when the user clicks the "CREATE" button"""
        dropdown_values = self.add_event_tab.get_dropdown_values()
        event_details = self.add_event_tab.get_event_details()

        self._add_event(dropdown_values, event_details)
        self.add_event_tab.clear_event_details()

    def _add_event(self, dropdown_values: list, event_details: str) -> None:
        """This function add an event to the database"""
        if (not self._is_validate_dropdown_values(dropdown_values)
            or not self.db_handler.is_time_available(*dropdown_values) or not event_details):
            self.tk_message_box.showerror("Error", "Invalid Event")
            return
        self.db_handler.add_event(*dropdown_values, event_details)
        self.tk_message_box.showinfo("Success", "Event created successfully")
    
    def _is_validate_dropdown_values(self, dropdown_values: list) -> bool:
        if any(value == "" for value in dropdown_values):
            return False
        start_time = datetime.strptime(f"{dropdown_values[0]}-{dropdown_values[1]}-{dropdown_values[2]} {dropdown_values[3]}", "%Y-%m-%d %I:%M %p")
        end_time = datetime.strptime(f"{dropdown_values[0]}-{dropdown_values[1]}-{dropdown_values[2]} {dropdown_values[4]}", "%Y-%m-%d %I:%M %p")
        if start_time > end_time:
            return False
        return True

    def on_click_all_event(self):
        """This function is called when the user clicks the "All Events" button"""
        # clear the listbox
        self.add_event_tab.clear_event_list()
        all_events = self.db_handler.get_all_events()
        if not all_events:
            self.tk_message_box.showinfo("Info", "No events found")
            return
        for event in all_events:
            formatted_event = self._format_event(event)
            self.add_event_tab.event_list.insert(tk.END, formatted_event)

    def on_click_search(self):
        """This function is called when the user clicks the "SEARCH" button"""
        self.retrieve_event_tab.clear_event_list()
        dropdpwn_values = self.retrieve_event_tab.get_dropdown_values()
        query = "SELECT * FROM events WHERE "
        events = self.db_handler.find_event(query, *dropdpwn_values)

        if not events:
            self.tk_message_box.showinfo("Info", "No events found")
            return
        for event in events:
            formatted_event = self._format_event(event)
            self.retrieve_event_tab.event_list.insert(tk.END, formatted_event)
    
    def on_click_search_in_delete(self):
        """This function is called when the user clicks the "SEARCH" button in the delete tab"""
        self.delete_event_tab.clear_event_list()
        dropdpwn_values = self.delete_event_tab.get_dropdown_values()
        query = "SELECT * FROM events WHERE "
        events = self.db_handler.find_event(query, *dropdpwn_values)

        if not events:
            self.tk_message_box.showinfo("Info", "No events found")
            return
        for event in events:
            formatted_event = self._format_event(event)
            self.delete_event_tab.event_list.insert(tk.END, formatted_event)

    def on_click_update(self):
        """This function is called when the user clicks the "UPDATE" button"""
        self.update_window = UpdateEventWindow(self.root, self.on_click_update_event)
    
    def on_click_update_event(self):
        """This function is called when the user clicks the "UPDATE" button
        inside the UpdateEventWindow"""
        event_id = self.update_window.get_event_id()
        updated_values = self.update_window.get_dropdown_values()
        updated_event_details = self.update_window.get_event_details()
        if not self._is_validate_dropdown_values(updated_values) or not updated_event_details:
            self.tk_message_box.showerror("Error", "Invalid Event")
            return
        self.db_handler.update_event(event_id, *updated_values, updated_event_details)
        self.update_window.close_window()
    
    def on_click_delete(self):
        """This function is called when the user clicks the "DELETE" button"""
        self.delete_event_tab.clear_event_list()
        dropdpwn_values = self.delete_event_tab.get_dropdown_values()
        query = "SELECT id FROM events WHERE "
        events = self.db_handler.find_event(query, *dropdpwn_values)
        self.tk_message_box.showinfo("Confirm", "Delete will remove all the events from the search result. Are you sure you want to delete?")
        self.db_handler.delete_event(events)
        self.delete_event_tab.clear_event_list()
    
    def on_click_delete_all(self):
        """This function is called when the user clicks the "DELETE ALL" button"""
        self.tk_message_box.showinfo("Confirm", "Delete will remove all the events. Are you sure you want to delete?")
        self.db_handler.clear_all_events()
        self.delete_event_tab.clear_event_list()

    def _create_navigation_tabs(self):
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
    
    def _format_event(self, event: list) -> str:
        """returns a formatted string of the event
            example output:
                id: 1 2023-01-01 12:00:00 - 13:00:00 : New Year's Day"""
        event_id, year, month, day, start_time, end_time, event_details = event
        formatted_event_id = f"{event_id:<5}"
        return f"EVENT_id: {formatted_event_id}{year}-{month}-{day} {start_time} - {end_time} : {event_details}"

    # TODO create menu bar: about, help, exit

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EventApp()
    app.db_handler.create_table()
    app.run()
    app.db_handler.close()