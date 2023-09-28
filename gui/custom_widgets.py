import tkinter as tk
from tkinter import ttk

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