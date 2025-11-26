# Pulse - Community Workout Tracker

## Overview
Pulse is a community workout tracking application that helps people stay active by logging and sharing their workouts. Built with Flask and SQLAlchemy.

## Project Architecture
- **Backend**: Flask web server with Jinja2 templates
- **ORM**: SQLAlchemy (prepared for PostgreSQL, currently using JSON storage)
- **Data Storage**: JSON file-based storage in `/data` directory
- **Server**: Runs on 0.0.0.0:5000

## Tech Stack
- Python 3.11
- Flask 3.x
- SQLAlchemy 2.x
- Gunicorn (production)
- Jinja2 templates
- File-based JSON storage (will migrate to PostgreSQL)

## Project Structure
```
/
├── app/                    # Flask application package
│   ├── __init__.py         # App factory
│   ├── routes.py           # URL routes and views
│   ├── models.py           # SQLAlchemy ORM models
│   ├── services/           # Business logic layer
│   │   └── storage.py      # JSON data repository
│   ├── templates/          # Jinja2 HTML templates
│   │   ├── base.html       # Base template
│   │   └── home.html       # Home page
│   └── static/             # Static assets
│       └── css/
│           └── app.css     # Application styles
├── data/                   # JSON data storage
│   └── workouts.json       # Workout data file
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── replit.md               # Project documentation
```

## Features
- Log workouts with name, type, duration, and notes
- View workout statistics (total workouts, total minutes, workouts this week)
- Community feed of recent workouts in reverse chronological order
- Delete workouts
- Responsive UI with purple gradient theme
- Both HTML form-based and JSON API endpoints

## API Endpoints
- GET `/api/workouts` - Fetch all workouts (JSON)
- POST `/api/workouts` - Create a new workout (JSON)
- DELETE `/api/workouts/:id` - Delete a workout (JSON)
- GET `/api/stats` - Get workout statistics (JSON)

## Web Routes
- GET `/` - Home page with workout list and stats
- POST `/workouts` - Create workout via HTML form
- POST `/workouts/<id>/delete` - Delete workout via HTML form

## Local Development
1. Create a virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`
5. Open http://localhost:5000

## Replit Development
Run `python main.py` to start the Flask dev server on port 5000.

## Production Deployment
Configured for Replit Autoscale deployment:
- Run command: `gunicorn --bind 0.0.0.0:5000 --reuse-port main:app`
- Port: 5000

## Data Migration Path
The app uses SQLAlchemy models prepared for PostgreSQL migration:
- `User` model with workouts relationship
- `Workout` model with type, duration, notes
- Currently backed by JSON file storage in `/data/workouts.json`
- Will migrate to PostgreSQL database when ready

## Recent Changes
- November 26, 2025: Converted from Node.js/React to Flask/SQLAlchemy
- November 26, 2025: Added SQLAlchemy models for future PostgreSQL migration
- November 26, 2025: Created Jinja2 templates matching original React UI
- November 25, 2025: Initial project setup from GitHub import
