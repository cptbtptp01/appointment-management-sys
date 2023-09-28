import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime

class CustomEntry(tk.Frame):
    """custom entry
        example usage:
        entry = CustomEntry(root, "your label")"""
    
    def __init__(self, master, label_text):
        super().__init__(master)

        self.label = ttk.Label(self, text=label_text)
        self.entry = ttk.Entry(self)

        self.label.pack(side=tk.LEFT)
        self.entry.pack(side=tk.RIGHT, fill = 'x')
    
    def get_text(self):
        return self.entry.get()

    def set_text(self, text):
        self.entry.set(text)

class CustomDropdown(tk.Frame):
    """custom dropdown menu
        example usage:
        options = ["option1", "option2", "option3"]
        dropdown = CustomDropdown(root, "your label", options)"""
    
    def __init__(self, master, label_text, options):
        super().__init__(master)

        self.label = ttk.Label(self, text=label_text)
        self.variable = tk.StringVar(self)
        self.variable.set(options[0])
        self.dropdown = ttk.Combobox(self, textvariable=self.variable, values=options)

        self.label.pack(side=tk.LEFT)
        self.dropdown.pack(side=tk.RIGHT, fill = 'x')
    
    def get_text(self):
        return self.variable.get()

    def set_text(self, text):
        self.variable.set(text)

class CustomLabel(tk.Frame):
    """custom label
        example usage:
        label = CustomLabel(root, "your label")"""
    
    def __init__(self, master, text):
        super().__init__(master)

        self.label = ttk.Label(self, text=text)

        self.label.pack(side=tk.LEFT)
    
    def get_text(self):
        return self.label.get()

    def set_text(self, text):
        self.label.set(text)

class CustomButton(tk.Frame):
    """custom button
        example usage:
        button = CustomButton(root, "your button text", command)
    """
    def __init__(self, master, text, command):
        super().__init__(master)

        self.button = ttk.Button(self, text=text, command=command)

        self.button.pack(side=tk.LEFT)

    def disable(self):
        self.button['state'] = tk.DISABLED

    def enable(self):
        self.button['state'] = tk.NORMAL

class DateTimeDropdown:
    """custom date and time dropdown"""

    """class variable for date and time dropdown"""
    year_options = [""]
    year_options += [str(year) for year in range(2023, 2030)]
    month_options = [""]
    month_options += [datetime(1900, month, 1).strftime('%b') for month in range(1, 13)]
    day_options = [""]
    day_options += [str(day) for day in range(1, 32)]
    time_options = [""]
    time_options += [f'{hour}:00 AM' if hour <= 12 else f'{hour - 12}:00 PM' for hour in range(1, 25)]
    
    def __init__(self, parent_frame) -> None:
        self.parent_frame = parent_frame
        self.create_date_time_dropdown()
    
    def create_date_time_dropdown(self) -> None:
        self.year_dropdown = CustomDropdown(self.parent_frame, "Year", self.year_options)
        self.month_dropdown = CustomDropdown(self.parent_frame, "Month", self.month_options)
        self.day_dropdown = CustomDropdown(self.parent_frame, "Day", self.day_options)
        self.start_time_dropdown = CustomDropdown(self.parent_frame, "Start Time", self.time_options)
        self.end_time_dropdown = CustomDropdown(self.parent_frame, "End Time", self.time_options)

        self.year_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.month_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.day_dropdown.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        
        self.start_time_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.end_time_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    
    def get_dropdown_values(self) -> list:
        """returns a list of values from the dropdowns
            example return value: ["2021", "Jan", "1", "1:00 AM", "2:00 AM"]"""
        month_num = list(calendar.month_abbr).index(self.month_dropdown.get_text())
        return [self.year_dropdown.get_text(), month_num, self.day_dropdown.get_text(), self.start_time_dropdown.get_text(), self.end_time_dropdown.get_text()]