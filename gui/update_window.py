import tkinter as tk
from tkinter import ttk
from gui.custom_widgets import DateTimeDropdown, CustomButton, CustomLabel, CustomEntry

class UpdateEventWindow():
    # prompt a window with entry label 'Event id:' [entry]
    # drop down for year, month, day, start time, end time
    # entry label 'Enter your event detail'
    # [entry]
    # [UPDATE] button - when click, perform on_click_update_event
    def __init__(self, root, on_click_update_event):
        self.root = tk.Toplevel(root)
        self.on_click_update_event = on_click_update_event
        self.create_update_event_window()
    
    def create_update_event_window(self):
        self.root.title("Update Event")
        root_frame = ttk.LabelFrame(self.root, text="Update Event")
        root_frame.grid(row=0, column=0, padx=8, pady=4)
        
        # dropdowns
        self.dropdown = DateTimeDropdown(root_frame)
        
        # event id entry
        self.event_id = CustomEntry(root_frame, "Enter event id")
        self.event_id.grid(column=0, row=2, pady=(10, 0), sticky="W")
        
        # event details entry
        event_label = CustomLabel(root_frame, "Enter your event details")
        event_label.grid(column=0, row=3, pady=(10, 0), sticky="W")
        self.event_details = ttk.Entry(root_frame, width=50)
        self.event_details.grid(column=0, row=4, pady=(10, 0), sticky="W")

        update_button = CustomButton(root_frame, "UPDATE", self.on_click_update_event)
        update_button.grid(column=0, row=5, pady=(10, 0), sticky="W")
    
    def get_dropdown_values(self) -> list:
        """returns a list of values from the dropdowns
        in the following order: year, month, day, start time, end time"""
        return self.dropdown.get_dropdown_values()
    
    def get_event_details(self) -> str:
        """returns the event details entered by the user"""
        return self.event_details.get()

    def get_event_id(self) -> str:
        """returns the event id entered by the user"""
        return self.event_id.get_text()
    
    def close_window(self):
        self.root.destroy()