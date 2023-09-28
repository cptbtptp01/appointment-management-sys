import tkinter as tk
from tkinter import ttk

class CustomDropdown(tk.Frame):
    """Custom dropdown menu"""

    def __init__(self, master, label_text, options):
        super().__init__(master)

        self.label = ttk.Label(self, text=label_text)
        self.variable = tk.StringVar(self)
        self.variable.set(options[0])
        self.dropdown = ttk.Combobox(self, textvariable=self.variable, values=options)

        self.label.pack(side=tk.LEFT)
        self.dropdown.pack(side=tk.RIGHT, fill='x')

    def get_text(self):
        return self.variable.get()

    def set_text(self, text):
        self.variable.set(text)

def on_dropdown_change(event):
    selected_option = dropdown.get_text()
    label.config(text=f"Selected: {selected_option}")

# Create a Tkinter window
root = tk.Tk()
root.title("Custom Dropdown Test")

# Define some options for the dropdown
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

# Create an instance of your CustomDropdown
dropdown = CustomDropdown(root, "Select an option:", options)
dropdown.pack(padx=20, pady=20)

# Create a label to display the selected option
label = tk.Label(root, text="Selected: ")
label.pack()

# Bind the dropdown change event to the on_dropdown_change function
dropdown.dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)

# Start the Tkinter main loop
root.mainloop()