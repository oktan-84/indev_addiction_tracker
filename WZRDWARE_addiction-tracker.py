
#an addiction tracker.

import json
import os
from datetime import datetime

#backend

urge_log = "urge_log.json"

def activity_log():
  if not os.path.exists(urge_log): #checks if the log file exists, if it doesn't then it makes it exist ig
    return[]
  with open(urge_log, "r") as f:
    return json.load(f)

def log_new_urge(intensity): #allows you to log a new urge with a HH:MM DD/MM/YYYY format
  load_logs = activity_log()
  time = datetime.now().strftime("%H:%M %d/%m/%Y")
  new_urge = { #how the .json file should be laid out
      "type": "urge",
      "datetime": time,
      "intensity": intensity
  }
  
  load_logs.append(new_urge)
  with open(urge_log, "w") as f:
    json.dump(load_logs, f, indent=4)
    print(f"Logged new urge successfully. [{time}]") #places the unlogged urge inside the .json file.

def log_new_relapse():
  load_logs = activity_log()
  time = datetime.now().strftime("%H:%M %d/%m/%Y")
  new_relapse = { #how the .json file should be laid out pt. 2
      "type": "relapse",
      "datetime": time
  }
  
  load_logs.append(new_relapse)
  with open(urge_log, "w") as f:
    json.dump(load_logs, f, indent=4)
    print(f"Logged new relapse successfully. [{time}]") #places the unlogged relapse inside the .json file.

def logstart(): #allows you to log a new urge with a HH:MM DD/MM/YYYY format
  load_logs = activity_log()
  time = datetime.now().strftime("%H:%M %d/%m/%Y")
  new_urge = { #how the .json file should be laid out
      "type": "CODE EXECUTION",
      "datetime": time,
  }
  
  load_logs.append(new_urge)
  with open(urge_log, "w") as f:
    json.dump(load_logs, f, indent=4)
    print(f"Logged started successfully. [{time}]") #places the unlogged urge inside the .json file.

def stats(): #calculates total number of urges and the date of your last urge. Not used as of yet.
  load_logs = activity_log()
  total_urges = len(load_logs)

  last_urge = load_logs[-1]
  return total_urges, f"{last_urge['datetime']}"

def show_logs(): #shows all logged urges, if none are found, returns a message saying so
  load_logs = activity_log()
  print(f"URGE LOG:")
  if not load_logs:
    print("No entries found.")
    return

  for index, entry in enumerate(load_logs, start=1):
    entry_type = entry.get("type", "urge") #if you have an older version without the type field, its treated as an urge (shouldnt because nobody else has used this as far as i know, but oh well)
    if entry_type == "urge":
      print(f"{index}. URGE | [{entry['datetime']}] | Intensity: {entry['intensity']}")
    elif entry_type == "relapse":
      print(f"{index}. RELAPSE | [{entry['datetime']}]")

def reset(): #clears all data from the log file
  with open(urge_log, "w") as f:
    json.dump([], f, indent=4)

def escalteurge(): #allows you to log a new urge with a HH:MM DD/MM/YYYY format
  load_logs = activity_log()
  time = datetime.now().strftime("%H:%M %d/%m/%Y")
  new_urge = { #how the .json file should be laid out
      "type": "PREVIOUS URGE ESCALATED",
      "datetime": time,
  }
  
  load_logs.append(new_urge)
  with open(urge_log, "w") as f:
    json.dump(load_logs, f, indent=4)
    print(f"Urge Escalated successfully. [{time}]") #places the unlogged urge inside the .json file.

logstart()

#frontend

colour = "lightgrey"
colour2 = "white"

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

root = tk.Tk() #creates main window
root.configure(background=f"{colour}")

root.title("WIZARDWARE ADDICTION TRACKER") #sets title

img = tk.PhotoImage(file = "image.png")
root.iconphoto(False, img)

root.geometry("550x550")
root.resizable(False, False)

with open(urge_log, "r") as f:
  c1 = json.load(f)
  c2 = activity_log()

logtitle = tk.Label(root, text="ACTIVITY LOG", font="Helvetica 20 bold")
logtitle.place(x=40, y=30)
logtitle.configure(background=f"{colour}")

log = scrolledtext.ScrolledText(root, width=50, height=20, font="Helvetica 12")
log.place(x=40, y=80)

def updatelog():
  log.configure(state="normal")
  log.delete(1.0, tk.END)

  logs = activity_log()

  if not logs:
    log.insert(tk.END, "No Entries Found")
  else:
    for index, entry in enumerate(logs, start=1):
      line = f"{index}.) {entry['type'].upper()} / [{entry['datetime']}]"
      if "intensity" in entry:
        line += f" / Intensity: {entry['intensity']}"
      log.insert(tk.END, line + "\n")

log.configure(state="disabled")

updatelog()

gurgebutton = tk.Button(root, text="GREEN URGE", font="bold", command=lambda: [log_new_urge("GREEN"), updatelog()])
gurgebutton.place(x=40, y=490)
gurgebutton.configure(background=f"{colour2}")

aurgebutton = tk.Button(root, text="AMBER URGE", font="bold", command=lambda: [log_new_urge("AMBER"), updatelog()])
aurgebutton.place(x=330, y=451)
aurgebutton.configure(background=f"{colour2}")

rurgebutton = tk.Button(root, text="RED URGE", font="bold", command=lambda: [log_new_urge("RED"), updatelog()])
rurgebutton.place(x=220, y=451)
rurgebutton.configure(background=f"{colour2}")

relapsebutton = tk.Button(root, text="RELAPSE", font="bold", command=lambda: [log_new_relapse(), updatelog()])
relapsebutton.place(x=120, y=451)
relapsebutton.configure(background=f"{colour2}")

resetbutton = tk.Button(root, text="RESET", font="bold", command=lambda: [reset() if messagebox.askyesno(title="RESET DATA", message="Reset Data? This cannot be undone.") else None, updatelog()])
resetbutton.place(x=40, y=451)
resetbutton.configure(background="red")

escalate = tk.Button(root, text="ESCALATE", font="bold", command=lambda: [escalteurge(), updatelog()])
escalate.place(x=170, y=490)
escalate.configure(background=colour2)

root.mainloop() #keeps it open
