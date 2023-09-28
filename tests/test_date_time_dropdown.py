import sys
import os

# Get the path to the project root (assuming this script is in the tests directory)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the project root to the Python path
sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk
from gui.custom_widgets import DateTimeDropdown

root = tk.Tk()
root.title("TEST")

test_dropdown = DateTimeDropdown(root)
test_button = ttk.Button(root, text="TEST", command=lambda: print(test_dropdown.get_dropdown_values()))
test_button.grid(row=1, column=0)
root.mainloop()