from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.services.storage import get_all_workouts, create_workout, delete_workout, get_stats

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    workouts = get_all_workouts()
    stats = get_stats()
    workouts_reversed = list(reversed(workouts))
    return render_template('home.html', workouts=workouts_reversed, stats=stats)

@main_bp.route('/api/workouts', methods=['GET'])
def api_get_workouts():
    workouts = get_all_workouts()
    return jsonify(workouts)

@main_bp.route('/api/workouts', methods=['POST'])
def api_create_workout():
    data = request.get_json()
    workout = create_workout(
        username=data.get('username'),
        workout_type=data.get('type'),
        duration=int(data.get('duration', 0)),
        notes=data.get('notes')
    )
    return jsonify(workout), 201

@main_bp.route('/api/workouts/<workout_id>', methods=['DELETE'])
def api_delete_workout(workout_id):
    delete_workout(workout_id)
    return jsonify({'success': True})

@main_bp.route('/api/stats', methods=['GET'])
def api_get_stats():
    stats = get_stats()
    return jsonify(stats)

@main_bp.route('/workouts', methods=['POST'])
def form_create_workout():
    username = request.form.get('username')
    workout_type = request.form.get('type')
    duration = request.form.get('duration')
    notes = request.form.get('notes')
    
    if username and workout_type and duration:
        create_workout(
            username=username,
            workout_type=workout_type,
            duration=int(duration),
            notes=notes
        )
    
    return redirect(url_for('main.home'))

@main_bp.route('/workouts/<workout_id>/delete', methods=['POST'])
def form_delete_workout(workout_id):
    delete_workout(workout_id)
    return redirect(url_for('main.home'))
