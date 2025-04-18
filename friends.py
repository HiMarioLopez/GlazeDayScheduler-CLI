import csv
from datetime import datetime

def load_friends(csv_path):
    friends = []
    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', skipinitialspace=True)
        for row in reader:
            name = row["name"].strip()
            birthday = parse_birthday(row["birthday"].strip())
            nickname = row.get("nickname", "").strip()
            # Store both name and nickname
            friends.append({
                "name": name,
                "birthday": birthday,
                "nickname": nickname if nickname else None
            })
    return friends

def parse_birthday(birthday_str):
    try:
        if len(birthday_str) == 10:
            dt = datetime.strptime(birthday_str, "%Y-%m-%d")
        elif len(birthday_str) == 5:
            dt = datetime.strptime(birthday_str, "%m-%d")
        else:
            raise ValueError
        return (dt.month, dt.day)
    except Exception:
        raise ValueError(f"Invalid birthday format: {birthday_str}")
