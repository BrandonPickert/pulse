import json
from datetime import datetime, timedelta, timezone
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

def parse_datetime(dt_string):
    if not dt_string:
        return None
    try:
        cleaned = dt_string.replace('Z', '+00:00')
        return datetime.fromisoformat(cleaned)
    except (ValueError, TypeError):
        return None

def get_all_workouts():
    data = read_data()
    workouts = data.get('workouts', [])
    for w in workouts:
        w['id'] = str(w.get('id', ''))
    return workouts

def create_workout(username, workout_type, duration, notes=None):
    data = read_data()
    new_workout = {
        'id': str(int(datetime.now().timestamp() * 1000)),
        'username': username,
        'type': workout_type,
        'duration': int(duration),
        'notes': notes or '',
        'createdAt': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    data['workouts'].append(new_workout)
    write_data(data)
    return new_workout

def delete_workout(workout_id):
    workout_id_str = str(workout_id)
    data = read_data()
    original_count = len(data['workouts'])
    data['workouts'] = [w for w in data['workouts'] if str(w.get('id', '')) != workout_id_str]
    write_data(data)
    return len(data['workouts']) < original_count

def get_stats():
    data = read_data()
    workouts = data.get('workouts', [])
    
    total_workouts = len(workouts)
    total_minutes = sum(int(w.get('duration', 0)) for w in workouts)
    
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    this_week = 0
    for w in workouts:
        created = parse_datetime(w.get('createdAt'))
        if created:
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            if created > week_ago:
                this_week += 1
    
    return {
        'totalWorkouts': total_workouts,
        'totalMinutes': total_minutes,
        'thisWeek': this_week
    }
