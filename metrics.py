from collections import defaultdict
from datetime import datetime
import json
import math

def compute_fairness_metrics(schedule, friends):
    bdays = {f["name"]: f["birthday"] for f in friends}
    friend_distances = defaultdict(list)
    for entry in schedule:
        name = entry["name"]
        glaze_date = entry["date"]
        bmonth, bday = bdays[name]
        bday_this_year = datetime(glaze_date.year, bmonth, bday)
        dist = abs((glaze_date - bday_this_year).days)
        if dist > 182:
            bday_next = datetime(glaze_date.year + 1, bmonth, bday)
            bday_prev = datetime(glaze_date.year - 1, bmonth, bday)
            dist = min(abs((glaze_date - bday_next).days), abs((glaze_date - bday_prev).days))
        friend_distances[name].append(dist)

    print("\nFairness Metrics:")
    all_distances = []
    metrics = {"friends": {}, "overall": {}}
    for name in sorted(friend_distances):
        dists = friend_distances[name]
        all_distances.extend(dists)
        avg = sum(dists) / len(dists)
        min_dist = min(dists)
        max_dist = max(dists)
        print(f"  {name}:")
        print(f"    Glazed {len(dists)} time(s)")
        print(f"    Avg distance from birthday: {avg:.1f} days")
        print(f"    Min/Max distance: {min_dist} / {max_dist} days")
        metrics["friends"][name] = {
            "glazed_count": len(dists),
            "avg_distance": avg,
            "min_distance": min_dist,
            "max_distance": max_dist,
            "all_distances": dists,
        }

    if all_distances:
        mean = sum(all_distances) / len(all_distances)
        min_all = min(all_distances)
        max_all = max(all_distances)
        stddev = math.sqrt(sum((x - mean) ** 2 for x in all_distances) / len(all_distances))
        print("\n  Overall schedule stats:")
        print(f"    Mean distance: {mean:.1f} days")
        print(f"    Min distance: {min_all} days")
        print(f"    Max distance: {max_all} days")
        print(f"    Stddev: {stddev:.2f} days")
        metrics["overall"] = {
            "mean_distance": mean,
            "min_distance": min_all,
            "max_distance": max_all,
            "stddev": stddev,
        }
    return metrics

def save_fairness_metrics_json(metrics, filename):
    # Convert any non-serializable types (e.g., sets) to lists
    def convert(obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        return obj
    with open(filename, "w") as f:
        json.dump(metrics, f, indent=2, default=convert)
