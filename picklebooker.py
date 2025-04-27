from tkinter import *
from tkinter import ttk
from schedule_booking import schedule_run

def schedule_booking():
    schedule_run(date.get(), time.get(), court.get(), duration.get())

root = Tk()
root.title("Picklebooker")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

date = StringVar()
date_entry = ttk.Entry(mainframe, width=12, textvariable=date)
date_entry.grid(column=2, row=1, sticky=(W, E))
ttk.Label(mainframe, text="Date").grid(column=3, row=1, sticky=(W, E))

time = StringVar()
time_entry = ttk.Entry(mainframe, width=12, textvariable=time)
time_entry.grid(column=2, row=2, sticky=(W, E))
ttk.Label(mainframe, text="Time").grid(column=3, row=2, sticky=(W, E))

court = StringVar()
court_entry = ttk.Entry(mainframe, width=12, textvariable=court)
court_entry.grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Court").grid(column=3, row=3, sticky=(W, E))

duration = StringVar(value="90")
duration_entry = ttk.Entry(mainframe, width=12, textvariable=duration)
duration_entry.grid(column=2, row=4, sticky=(W, E))
ttk.Label(mainframe, text="Duration").grid(column=3, row=4, sticky=(W, E))


ttk.Button(mainframe, text="Schedule booking", command=schedule_booking).grid(column=2, row=7, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

date_entry.focus()

root.bind("<Return>", schedule_booking)

root.mainloop()