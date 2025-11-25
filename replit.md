# Pulse - Community Workout Tracker

## Overview
Pulse is a community workout tracking application that helps people stay active by logging and sharing their workouts. Built with React and Express.js.

## Project Architecture
- **Frontend**: React with Vite (runs on port 5000)
- **Backend API**: 
  - Development: Integrated into Vite via middleware plugin
  - Production: Express.js server serving both API and static files
- **Data Storage**: Shared JSON file-based storage in `/data` directory
- **Dev Server**: Configured to run on 0.0.0.0:5000

## Tech Stack
- Node.js 20
- React 18
- Vite 5
- Express.js 4
- File-based JSON storage (persistent across dev/prod)

## Project Structure
```
/
├── src/              # React frontend source
│   ├── App.jsx       # Main app component
│   ├── App.css       # App styles
│   ├── main.jsx      # React entry point
│   └── index.css     # Global styles
├── server/           # Backend code
│   ├── data.js       # Shared data access layer
│   ├── prod.js       # Production server
│   └── index.js      # Standalone API server (optional)
├── data/             # JSON data storage (gitignored except .gitkeep)
├── index.html        # HTML entry point
├── vite.config.js    # Vite configuration with API middleware
└── package.json      # Dependencies
```

## Features
- Log workouts with name, type, duration, and notes
- View workout statistics (total workouts, total minutes, workouts this week)
- Community feed of recent workouts in reverse chronological order
- Delete workouts
- Real-time stats updates
- Responsive UI with purple gradient theme

## API Endpoints
- GET `/api/workouts` - Fetch all workouts
- POST `/api/workouts` - Create a new workout
- DELETE `/api/workouts/:id` - Delete a workout
- GET `/api/stats` - Get workout statistics

## Development
Run `npm run dev` to start the Vite dev server with integrated API on port 5000.

## Production
1. Build: `npm run build` - Creates optimized production bundle in `/dist`
2. Start: `npm run start` - Runs Express server serving API and static files on port 5000

## Deployment
Configured for Replit Autoscale deployment:
- Build command: `npm run build`
- Run command: `npm run start`
- Port: 5000

## Recent Changes
- November 25, 2025: Initial project setup from GitHub import
- November 25, 2025: Fixed data persistence issue by creating shared data.js module
- All environments (dev/prod) now use the same `/data/workouts.json` file
