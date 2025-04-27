from datetime import datetime
from tkinter import *
from tkinter import ttk
from schedule_booking import schedule_run
from tkinter import messagebox

def schedule_booking(*args):
    if not validate_inputs():
        return
    schedule_run(date.get(), time.get(), int(court.get()), int(duration.get()))
    messagebox.showinfo(title="Success", message="Booking scheduler successfully created!")
    root.destroy()

def validate_inputs():
    try:
        datetime.strptime(date.get(), "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Input", "Date must be in YYYY-MM-DD format.")
        return False

    try:
        datetime.strptime(time.get(), "%H:%M")
    except ValueError:
        messagebox.showerror("Invalid Input", "Time must be in HH:MM (24-hour) format.")
        return False

    if court.get() not in ("1", "2", "3"):
        messagebox.showerror("Invalid Input", "Court must be 1, 2, or 3.")
        return False

    if duration.get() not in ("30", "60", "90"):
        messagebox.showerror("Invalid Input", "Duration must be 30, 60, or 90 minutes.")
        return False

    return True

    
root = Tk()
root.title("Picklebooker")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

date = StringVar()
date_entry = ttk.Entry(mainframe, width=12, textvariable=date)
date_entry.grid(column=1, row=1, sticky=(W, E))
ttk.Label(mainframe, text="Date").grid(column=2, row=1, sticky=(W, E))

time = StringVar()
time_entry = ttk.Entry(mainframe, width=12, textvariable=time)
time_entry.grid(column=1, row=2, sticky=(W, E))
ttk.Label(mainframe, text="Time").grid(column=2, row=2, sticky=(W, E))

court = StringVar()
court_entry = ttk.Combobox(mainframe, width=12, textvariable=court, values=["1", "2", "3"])
court_entry.grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Court").grid(column=2, row=3, sticky=(W, E))

duration = StringVar(value="90")
duration_entry = ttk.Combobox(mainframe, width=12, textvariable=duration, values=["30", "60", "90"])
duration_entry.grid(column=1, row=4, sticky=(W, E))
ttk.Label(mainframe, text="Duration").grid(column=2, row=4, sticky=(W, E))

ttk.Button(mainframe, text="Schedule booking", command=schedule_booking).grid(column=1, row=5, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

date_entry.focus()

root.bind("<Return>", schedule_booking)

root.mainloop()