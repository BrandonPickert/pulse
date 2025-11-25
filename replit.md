# Pulse - Community Workout Tracker

## Overview
Pulse is a community workout tracking application that helps people stay active by logging and sharing their workouts. Built with React and Express.js.

## Project Architecture
- **Frontend**: React with Vite (runs on port 5000)
- **Backend**: Express.js API (runs on port 3001)
- **Data Storage**: JSON file-based storage in `/data` directory
- **Dev Server**: Configured to run on 0.0.0.0:5000 with proxy to backend

## Tech Stack
- Node.js 20
- React 18
- Vite 5
- Express.js 4
- File-based JSON storage

## Project Structure
```
/
├── src/              # React frontend source
│   ├── App.jsx       # Main app component
│   ├── App.css       # App styles
│   ├── main.jsx      # React entry point
│   └── index.css     # Global styles
├── server/           # Express backend
│   └── index.js      # API server
├── data/             # JSON data storage
├── index.html        # HTML entry point
├── vite.config.js    # Vite configuration
└── package.json      # Dependencies

```

## Features
- Log workouts with type, duration, and notes
- View workout statistics (total workouts, minutes, weekly count)
- Community feed of recent workouts
- Delete workouts
- Real-time stats updates

## API Endpoints
- GET `/api/workouts` - Fetch all workouts
- POST `/api/workouts` - Create a new workout
- DELETE `/api/workouts/:id` - Delete a workout
- GET `/api/stats` - Get workout statistics

## Setup Date
November 25, 2025 - Initial project setup from GitHub import
