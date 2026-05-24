
#an addiction tracker.

import json
import os
from datetime import datetime
import numpy as np

urge_log = "urge_log.json"

insult1 = (["Pathetic.", "Can't make it a day without crawling back like some kind of fucking junkie.", "Another urge? You genuinely are a waste of space, aren't you?", "Weak. So fucking weak.", "I bet you'll relapse before the sun comes down.", "You're worthless. Everyone knows it. Even deep down, somewhere in that impietous heart of yours, you know it too."])

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
    print(np.random.choice(insult1))

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
    print(np.random.choice(insult1))

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

print()
print("WELCOME TO THE WIZARDWARE™ ADDICTION TRACKER (INDEV | CLI)") #welcome message because friendly
print()
print("If you are unsure, enter 'help'")

while True:
  print()
  user_input = input("> ") #takes input of 'help, 1, 2, 3, or 4 then performs associated action
  print()
  if user_input == "help":
    print()
    print("OPTIONS DASHBOARD:")
    print("1.) LOG URGE")
    print("2.) LOG RELAPSE")
    print("3.) RESET")
    print("4.) OPEN URGE LOGS")
    print("5.) EXIT")
    print("(SELECT NUMBER OF DESIRED OPTION)")
    print()
  elif user_input == "1":
    colour = input("Intensity? (r/a/g) ") #assigns intensity value to urge
    if colour == "r":
      log_new_urge("Red")
    elif colour == "a":
      log_new_urge("Amber")
    elif colour == "g":
      log_new_urge("Green")
    else:
      print("INVALID")
  elif user_input == "2":
    log_new_relapse()
  elif user_input == "3":
    confirm = input(f"Are you sure? y/N ") #makes sure youre 100% sure about removing your data
    if confirm == "y" or confirm == "Y":
      reset()
    else:
      print("Action aborted or input invalid. Nothing has been changed.")
  elif user_input == "4":
    show_logs()
  elif user_input == "5": #kills the program
    break
  else:
    print("INVALID")
