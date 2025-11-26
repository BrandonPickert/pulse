#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta
from garminconnect import Garmin, GarminConnectAuthenticationError
import secrets

# ================================================================
# EDIT THESE TWO LINES ONLY THE FIRST TIME
# ================================================================
SECRETS_PATH = "secrets.json"
with open(SECRETS_PATH) as f:
    secrets = json.load(f)

EMAIL = secrets["garmin"]["email"]  # ← Your real Garmin email
PASSWORD = secrets["garmin"]["password"]  # ← Your real Garmin password
# ================================================================

# How many days back to fetch (180 = last 6 months, None = all time)
DAYS_BACK = 180

# Output file for your Replit app
OUTPUT_FILE = "server/data.json"


def login():
    """
    Logs in with email/password (opens browser for OAuth confirmation once).
    After first run, uses cached tokens (no browser/password needed).
    """
    try:
        # Try cached tokens first (no credentials needed)
        print("Trying cached tokens...")
        client = Garmin()
        client.login()
        print("Logged in with cached tokens!")
        return client
    except GarminConnectAuthenticationError:
        print("No cached tokens found. Starting OAuth flow...")
        print("This will open your browser for login (including 2FA if enabled).")
        print("After you confirm, tokens will be cached forever.")

        # Use email/password to initiate OAuth (library handles the rest)
        client = Garmin(EMAIL, PASSWORD)
        client.login()
        print("OAuth login successful! Tokens cached in ~/.garminconnect")
        return client


def main():
    if EMAIL == "your@email.com" or PASSWORD == "your_garmin_password":
        print("ERROR: Edit EMAIL and PASSWORD in the script first!")
        return

    client = login()

    # Fetch activities
    print(f"\nFetching last {DAYS_BACK or 'all'} days of activities...")
    if DAYS_BACK:
        start_date = (datetime.today() - timedelta(days=DAYS_BACK)).strftime("%Y-%m-%d")
        activities = client.get_activities_by_date(start_date, None)
    else:
        # For all-time, fetch in batches
        activities = client.get_activities(0, 10000)

    print(f"Downloaded {len(activities)} activities")

    # Convert to your app's format
    workouts = []
    for act in activities:
        workouts.append({
            "id": str(act["activityId"]),
            "name": act.get("activityName") or "Unnamed Activity",
            "type": act.get("activityType", {}).get("typeKey", "unknown"),
            "duration": round(act.get("duration", 0)),
            "distance": round(act.get("distance", 0)),
            "calories": act.get("calories"),
            "avgHR": act.get("averageHR"),
            "maxHR": act.get("maxHR"),
            "steps": act.get("steps"),
            "elevationGain": act.get("elevationGain"),
            "createdAt": act["startTimeLocal"],
        })

    os.makedirs("server", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"workouts": workouts, "lastUpdated": datetime.now().isoformat()}, f, indent=2)

    print(f"\nSaved {len(workouts)} real workouts → {OUTPUT_FILE}")
    print("Upload the 'server' folder to Replit → your app works instantly!")
    print("\nFirst 3 workouts:")
    for w in workouts[:3]:
        date = w["createdAt"][:10]
        name = w["name"]
        dist = w["distance"] / 1000
        mins = w["duration"] // 60
        print(f"   {date} | {name} | {dist:.2f} km | {mins} min")


if __name__ == "__main__":
    main()