import json
import os
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / 'data'
DATA_FILE = DATA_DIR / 'workouts.json'

def ensure_data_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({'workouts': [], 'users': []}))

def read_data():
    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    ensure_data_file()
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_all_workouts():
    data = read_data()
    return data.get('workouts', [])

def create_workout(username, workout_type, duration, notes=None):
    data = read_data()
    new_workout = {
        'id': str(int(datetime.now().timestamp() * 1000)),
        'username': username,
        'type': workout_type,
        'duration': duration,
        'notes': notes,
        'createdAt': datetime.now().isoformat()
    }
    data['workouts'].append(new_workout)
    write_data(data)
    return new_workout

def delete_workout(workout_id):
    data = read_data()
    data['workouts'] = [w for w in data['workouts'] if w['id'] != workout_id]
    write_data(data)
    return True

def get_stats():
    data = read_data()
    workouts = data.get('workouts', [])
    
    total_workouts = len(workouts)
    total_minutes = sum(w.get('duration', 0) for w in workouts)
    
    week_ago = datetime.now() - timedelta(days=7)
    this_week = 0
    for w in workouts:
        try:
            created = datetime.fromisoformat(w.get('createdAt', ''))
            if created > week_ago:
                this_week += 1
        except (ValueError, TypeError):
            pass
    
    return {
        'totalWorkouts': total_workouts,
        'totalMinutes': total_minutes,
        'thisWeek': this_week
    }
