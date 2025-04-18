from datetime import datetime
import sys
import os

from .friends import load_friends
from .storage import load_schedule, print_schedule, save_schedule
from .metrics import compute_fairness_metrics, save_fairness_metrics_json
from .scheduler import (
    greedy_maximize_birthday_distance,
    patch_schedule,
    patch_schedule_with_new_friend,
)

DEFAULT_CSV_PATH = "GlazeDayScheduler-CLI/data/friends.csv"
OUTPUT_DIR = "./GlazeDayScheduler-CLI/output"
SCHEDULE_FILENAME = "glaze_day_schedule.json"
METRICS_FILENAME = "glaze_day_fairness_metrics.json"

DEFAULT_BUFFER_DAYS = 1
DEFAULT_INTERVAL_DAYS = 7
DEFAULT_CYCLES = 1

def main():
    if len(sys.argv) < 2:
        print(f"No CSV path provided, using default: {DEFAULT_CSV_PATH}")
        csv_path = DEFAULT_CSV_PATH
    else:
        csv_path = sys.argv[1]
        
    friends = load_friends(csv_path)

    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d")
    print("Options:")
    print("1. Generate new schedule")
    print("2. Patch existing schedule (if a friend leaves)")
    print("3. Patch existing schedule (if a friend is added)")
    choice = input("Choose option [1/2/3, default 1]: ").strip() or "1"

    buffer_days_str = input(
        f"Enter birthday buffer (days) [default: {DEFAULT_BUFFER_DAYS}]: "
    ).strip()
    buffer_days = int(buffer_days_str) if buffer_days_str else DEFAULT_BUFFER_DAYS

    interval_days_str = input(
        f"Enter interval between glazes (days) [default: {DEFAULT_INTERVAL_DAYS}]: "
    ).strip()
    interval_days = int(interval_days_str) if interval_days_str else DEFAULT_INTERVAL_DAYS

    cycles_str = input(
        f"How many cycles? [default {DEFAULT_CYCLES}]: "
    ).strip()
    cycles = int(cycles_str) if cycles_str else DEFAULT_CYCLES

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    schedule_file = os.path.join(OUTPUT_DIR, SCHEDULE_FILENAME)
    metrics_file = os.path.join(OUTPUT_DIR, METRICS_FILENAME)

    if choice in ("2", "3"):
        if not os.path.exists(schedule_file):
            print(f"No existing schedule found at {schedule_file}.")
            sys.exit(1)
        old_schedule = load_schedule(schedule_file)
        if choice == "2":
            patched_schedule = patch_schedule(
                old_schedule, friends, today, buffer_days, interval_days
            )
        else:
            patched_schedule = patch_schedule_with_new_friend(
                old_schedule, friends, today, buffer_days, interval_days
            )
        print_schedule(patched_schedule, friends)
        metrics = compute_fairness_metrics(patched_schedule, friends)
        save_fairness_metrics_json(metrics, metrics_file)
        for entry in patched_schedule:
            entry["date"] = entry["date"].strftime("%Y-%m-%d")
        save_schedule(patched_schedule, schedule_file)
    else:
        start_date_str = input(
            f"Enter start date (YYYY-MM-DD) [default: today ({today_str})]: "
        ).strip()
        if not start_date_str:
            start_date_str = today_str
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        schedule = greedy_maximize_birthday_distance(
            friends, start_date, buffer_days, interval_days, cycles
        )
        for entry in schedule:
            entry["date"] = datetime.strptime(entry["date"], "%Y-%m-%d")
        print_schedule(schedule, friends)
        metrics = compute_fairness_metrics(schedule, friends)
        save_fairness_metrics_json(metrics, metrics_file)
        for entry in schedule:
            entry["date"] = entry["date"].strftime("%Y-%m-%d")
        save_schedule(schedule, schedule_file)

if __name__ == "__main__":
    main()
