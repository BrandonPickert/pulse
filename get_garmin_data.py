# get_garmin_data.py
import json
import os
from datetime import datetime
from garminconnect import Garmin  # pip install garminconnect

DATA_FILE = "data/workouts.json"

def load_existing_workouts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return {w["id"]: w for w in data.get("workouts", [])}
    return {}

def save_workouts(workouts_dict):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump({"workouts": list(workouts_dict.values())}, f, indent=2)

def sync_garmin(email, password):
    try:
        client = Garmin(email, password)
        client.login()

        activities = client.get_activities(0, 100)  # last 100

        existing = load_existing_workouts()
        added = 0

        for act in activities:
            act_id = str(act.get("activityId"))
            if act_id in existing:
                continue

            workout = {
                "id": act_id,
                "name": act.get("activityName"),
                "type": act.get("activityType", {}).get("typeKey", "other").capitalize(),
                "duration": int(act.get("duration", 0)),
                "distance": act.get("distance"),
                "calories": act.get("calories"),
                "avgHR": act.get("averageHR"),
                "maxHR": act.get("maxHR"),
                "steps": act.get("steps"),
                "elevationGain": act.get("elevationGain"),
                "createdAt": act.get("startTimeLocal", datetime.now().isoformat())
            }
            existing[act_id] = workout
            added += 1

        save_workouts(existing)
        return {"success": True, "added": added, "total": len(existing)}
    except Exception as e:
        return {"success": False, "error": str(e)}