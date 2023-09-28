import tkinter as tk
from tkinter import ttk
from gui.custom_widgets import DateTimeDropdown, CustomButton, CustomLabel

# comment out the following line when running tests
# from custom_widgets import DateTimeDropdown, CustomButton

class AddEventTab:
    """This class is responsible for creating the "Add Event" tab"""
    def __init__(self, root, on_click_create, on_click_all_event, on_click_update):
        self.root = root
        self.on_click_create = on_click_create
        self.on_click_all_event = on_click_all_event
        self.on_click_update = on_click_update
        self.create_add_event_tab()

    def create_add_event_tab(self):
        # Create a label frame
        root1 = ttk.LabelFrame(self.root, text="Add Event")
        root1.grid(row=0, column=0, padx=8, pady=4)
        
        # Create dropdowns for year, month, day, start time, and end time
        self.dropdown = DateTimeDropdown(root1)

        # Create event name label and entry
        event_label = CustomLabel(root1, "Enter your event details")
        event_label.grid(column=0, row=2, pady=(10, 0), sticky="W")
        self.event_details = ttk.Entry(root1, width=50)
        self.event_details.grid(column=0, row=3, pady=(10, 0), sticky="W")

        # Create listbox for displaying all events
        self.event_list = tk.Listbox(root1, height=15, width=50)
        self.event_list.grid(column=0, row=4, pady=(10, 0), sticky="W")

        # Create the "CREATE", "UPDATE" and "All Events" buttons
        create_button = CustomButton(root1, "CREATE", self.on_click_create)
        create_button.grid(column=0, row=5, pady=(10, 0), sticky="W")
        view = CustomButton(root1, "All Events", self.on_click_all_event)
        view.grid(column=0, row=6, pady=(10, 0), sticky="W")
        update_button = CustomButton(root1, "UPDATE", self.on_click_update)
        update_button.grid(column=0, row=7, pady=(10, 0), sticky="W")
    
    def get_event_details(self) -> str:
        """returns the event details entered by the user"""
        return self.event_details.get()
    
    def get_dropdown_values(self) -> list:
        """returns a list of values from the dropdowns
        in the following order: year, month, day, start time, end time"""
        return self.dropdown.get_dropdown_values()

    def clear_event_details(self):
        self.event_details.delete(0, tk.END)
    
    def clear_event_list(self):
        self.event_list.delete(0, tk.END)


if __name__ == "__main__":
    test_root = tk.Tk()
    test_root.title("TEST")
    test_add_event_tab = AddEventTab(test_root, lambda: print("CREATE"), lambda: print("ALL EVENTS"))
    test_root.mainloop()