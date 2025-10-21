# TODO App

## Overview
A simple TODO application with a TypeScript React frontend and Python Flask backend. The application uses Replit's key-value database for persistent storage.

## Recent Changes
- **October 21, 2025**: Initial project setup
  - Created TypeScript React frontend with Vite
  - Built Python Flask backend with RESTful API
  - Integrated Replit Database for persistent storage
  - Configured workflows for both frontend and backend

## Project Architecture

### Frontend (TypeScript + React)
- **Location**: `/src`
- **Port**: 5000 (Vite dev server)
- **Tech Stack**: React 19, TypeScript, Vite
- **Features**:
  - Create, read, update, and delete TODOs
  - Mark tasks as complete/incomplete
  - Real-time UI updates
  - Clean, modern interface with gradient background

### Backend (Python + Flask)
- **Location**: `/server`
- **Port**: 8080
- **Tech Stack**: Python 3.11, Flask, Flask-CORS
- **Features**:
  - RESTful API endpoints
  - Persistent key-value storage using Replit Database
  - CORS-enabled for cross-origin requests

### Database
- **Type**: Replit Database (key-value store)
- **Storage**: TODOs stored with prefix `todo:{id}`
- **Data Format**: JSON strings

## API Endpoints

- `GET /api/todos` - Retrieve all todos
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/<id>` - Update a todo
- `DELETE /api/todos/<id>` - Delete a todo
- `GET /api/health` - Health check endpoint

## File Structure
```
.
├── server/
│   └── app.py              # Flask backend application
├── src/
│   ├── main.tsx            # React entry point
│   ├── App.tsx             # Main App component
│   ├── App.css             # App styles
│   └── index.css           # Global styles
├── index.html              # HTML template
├── vite.config.ts          # Vite configuration
├── tsconfig.json           # TypeScript configuration
├── package.json            # Node.js dependencies
└── pyproject.toml          # Python dependencies
```

## Running the Application

The application runs automatically with two workflows:
1. **Backend** - Python Flask server on port 8080
2. **Frontend** - Vite dev server on port 5000

Both workflows start automatically when the Repl runs.

## User Preferences
None specified yet.
