# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime, timedelta
from get_garmin_data import sync_garmin, load_existing_workouts

app = Flask(__name__)
app.secret_key = "super-secret-pulse-key-2025"  # change in prod!

def get_user_workouts():
    workouts = load_existing_workouts().values()
    return sorted(workouts, key=lambda x: x["createdAt"], reverse=True)

def calculate_streak(workouts):
    if not workouts:
        return 0
    dates = sorted({w["createdAt"][:10] for w in workouts})
    if not dates:
        return 0

    today = datetime.today().date()
    streak = 0
    expected = today

    for date_str in reversed(dates):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if date == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif date < expected:
            break
    return streak

@app.route("/")
def index():
    workouts = list(get_user_workouts())[:20]
    total_mins = sum(w["duration"] for w in workouts) // 60
    streak = calculate_streak(workouts)

    stats = {
        "totalWorkouts": len(workouts),
        "totalMinutes": total_mins,
        "thisWeek": len([w for w in workouts if (datetime.now().date() - datetime.strptime(w["createdAt"][:10], "%Y-%m-%d").date()).days <= 7]),
        "streak": streak
    }
    return render_template("index.html", workouts=workouts, stats=stats)

@app.route("/connect-garmin", methods=["GET", "POST"])
def connect_garmin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        result = sync_garmin(email, password)
        if result["success"]:
            flash(f"Garmin synced! {result['added']} new workouts added. Total: {result['total']}", "success")
        else:
            flash(f"Error: {result['error']}", "error")
        return redirect(url_for("index"))
    return render_template("garmin_connect.html")

if __name__ == "__main__":
    app.run(debug=True)