import tkinter as tk
from tkinter import ttk
from gui.custom_widgets import DateTimeDropdown, CustomButton, CustomLabel

# comment out the following line when running tests
# from custom_widgets import DateTimeDropdown, CustomButton

class DeleteEventTab:
    """This class is responsible for creating the "Delete Event" tab"""
    def __init__(self, root, on_click_search, on_click_delete):
        self.root = root
        self.on_click_search = on_click_search
        self.on_click_delete = on_click_delete
        self.create_delete_event_tab()
    
    def create_delete_event_tab(self):
        root1 = ttk.LabelFrame(self.root, text="Delete Event")
        root1.grid(row=0, column=0, padx=8, pady=4)

        self.dropdown = DateTimeDropdown(root1)

        instruction_label = CustomLabel(root1, "Note: Please select at least one of the following options to delete event")
        instruction_label.grid(column=0, row=2, pady=(10, 0), sticky="W")

        self.event_list = tk.Listbox(root1, height=15, width=50)
        self.event_list.grid(column=0, row=3, pady=(10, 0), sticky="W")

        search_button = CustomButton(root1, "SEARCH", self.on_click_search)
        delete_button = CustomButton(root1, "DELETE", self.on_click_delete)
        search_button.grid(column=0, row=4, pady=(10, 0), sticky="W")
        delete_button.grid(column=0, row=5, pady=(10, 0), sticky="W")
    
    def get_dropdown_values(self) -> list:
        """returns a list of values from the dropdowns
        in the following order: year, month, day, start time, end time"""
        return self.dropdown.get_dropdown_values()
    
    def clear_event_list(self):
        self.event_list.delete(0, tk.END)