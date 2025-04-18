from datetime import datetime, timedelta
from .utils import days_between, is_within_buffer

def greedy_maximize_birthday_distance(friends, start_date, buffer_days, interval_days, cycles=1):
    schedule = []
    for cycle in range(cycles):
        available_friends = friends.copy()
        current_date = start_date + timedelta(days=cycle * len(friends) * interval_days)
        for _ in range(len(friends)):
            candidates = [
                f for f in available_friends
                if not is_within_buffer(current_date, f["birthday"], buffer_days)
            ]
            if not candidates:
                candidates = available_friends
                note = "Within birthday buffer!"
            else:
                note = None
            best_friend = max(
                candidates,
                key=lambda f: days_between(
                    current_date, datetime(current_date.year, f["birthday"][0], f["birthday"][1])
                ),
            )
            entry = {"date": current_date.strftime("%Y-%m-%d"), "name": best_friend["name"]}
            if note:
                entry["note"] = note
            schedule.append(entry)
            available_friends.remove(best_friend)
            current_date += timedelta(days=interval_days)
    return schedule

def patch_schedule(old_schedule, friends, today, buffer_days, interval_days):
    patched = [entry for entry in old_schedule if entry["date"] < today]
    already_glazed = {entry["name"] for entry in patched}
    remaining_friends = [f for f in friends if f["name"] not in already_glazed]
    if patched:
        next_date = patched[-1]["date"] + timedelta(days=interval_days)
    else:
        next_date = today
    future_schedule = greedy_maximize_birthday_distance(
        remaining_friends, next_date, buffer_days, interval_days, cycles=1
    )
    for entry in future_schedule:
        entry["date"] = datetime.strptime(entry["date"], "%Y-%m-%d")
    return patched + future_schedule

def patch_schedule_with_new_friend(old_schedule, friends, today, buffer_days, interval_days):
    return patch_schedule(old_schedule, friends, today, buffer_days, interval_days)
