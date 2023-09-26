import tkinter

root = tkinter.Tk()

# creating label widget
myLabel = tkinter.Label(root, text="Appointment Scheduler")
# shoving onto screen
myLabel.pack()

# event loop
root.mainloop()