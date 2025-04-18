import json
from datetime import datetime

def save_schedule(schedule, filename):
    with open(filename, "w") as f:
        json.dump(schedule, f, indent=2)

def load_schedule(filename):
    with open(filename, "r") as f:
        schedule = json.load(f)
    for entry in schedule:
        entry["date"] = datetime.strptime(entry["date"], "%Y-%m-%d")
    return schedule

def print_schedule(schedule, friends):
    print("\nGlaze Schedule:")
    # Build a lookup for fast access
    name_to_friend = {f["name"]: f for f in friends}
    for entry in schedule:
        friend = name_to_friend.get(entry["name"], {})
        display_name = friend.get("nickname") or entry["name"]
        line = f"{entry['date'].strftime('%Y-%m-%d')}: {display_name}"
        if "note" in entry:
            line += f" ({entry['note']})"
        print(line)
