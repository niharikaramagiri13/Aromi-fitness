# 🌿 Aromi AI Wellness Assistant

Aromi is a Django-based wellness and fitness web application designed to help users track health goals, log daily activity, monitor progress, and get responsive fitness guidance through an AI-style chatbot.

## 🔎 Overview

This project is a complete personal wellness dashboard built with Django. Users can:

- create an account and sign in
- complete a health profile onboarding flow
- generate a personalized fitness plan based on age, height, weight, goal, and activity profile
- log workouts, weight, water intake, calories, steps, mood, and notes
- view progress charts and wellness statistics over time
- use a chatbot to ask questions related to nutrition, workouts, fatigue, injury support, sleep, and motivation

## 🎯 Project Purpose

Aromi combines three main ideas:

1. Health profile management
2. Daily fitness habit tracking
3. Personalized guidance via an interactive wellness assistant

The app is intended for people who want a simple way to manage fitness routines and health data in one place.

## 🛠️ Tech Stack

- Python
- Django 6.0.5
- SQLite database
- HTML / CSS / Django Templates
- Bootstrap-style custom frontend styling in the static files

## 📁 Project Structure

```text
aromi/
├── aromi/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── wellness_app/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── static/
│       └── css/
│           └── ...
└── templates/
    └── ...
```

### 🧩 Main Application Modules

#### `aromi/`
This folder contains the Django project configuration:

- `settings.py`: project settings, installed apps, database configuration, templates, and static files
- `urls.py`: project-wide routing
- `asgi.py` and `wsgi.py`: ASGI/WSGI deployment entry points

#### `wellness_app/`
This is the main app where most of the functionality lives:

- `models.py`: core data models for user profile and fitness logs
- `views.py`: login, dashboard, plan, log, progress, history, chatbot, and logout flows
- `urls.py`: route mapping for all dashboard pages and chatbot endpoints
- `templates/`: HTML pages for the user interface
- `static/css/`: page-specific styling for login, register, dashboard, plan, progress, chatbot, history, and log pages

## ✨ Core Features

### 1. User Authentication
Users can register, login, and logout through Django authentication.

### 2. Health Profile Onboarding
The dashboard collects:

- age
- height
- weight
- health goal
- gender
- activity level
- diet preference
- health conditions

This profile becomes the foundation for generating personalization.

### 3. Personalized Fitness Plan
The `plan` screen calculates:

- BMI
- BMI category
- daily calorie target
- water target
- protein target
- workout schedule recommendation

### 4. Daily Fitness Logging
Users can submit daily wellness data such as:

- weight
- calories
- steps
- water intake
- workout type
- workout duration
- workout intensity
- mood
- notes

The app stores a single daily log per user, making it easy to maintain a continuous activity record.

### 5. Progress Tracking
The `progress` view provides:

- recent 30-day activity timeline
- chart data for weight, calories, water, steps, and mood
- total logs count
- average water intake
- average steps
- current streak of activity
- weight change calculation

### 6. History View
A history page lists all stored user logs for review.

### 7. Wellness Chatbot
The chatbot endpoint responds with health and fitness guidance based on message keywords. It supports common topics such as:

- weight loss
- muscle gain
- protein advice
- hydration
- cardio guidance
- workout planning
- fever, pain, fatigue, and sleep support
- stress and motivation support

## 🗂️ Data Models

### `UserHealthProfile`
Stores the user's health profile and personal goal information.

Fields include:

- `user` (OneToOne with Django user)
- `age`
- `height`
- `weight`
- `goal`
- `gender`
- `activity`
- `diet`
- `conditions`

### `FitnessLog`
Stores the user's daily wellness log.

Fields include:

- `user`
- `date`
- `weight`
- `calories`
- `steps`
- `water`
- `workout`
- `duration`
- `intensity`
- `mood`
- `notes`
- `created`

The model enforces one log entry per user per date.

## 🧭 Routes

The app defines the following primary routes:

- `/` → Home page
- `/login/` → Login page
- `/register/` → Registration page
- `/dashboard/` → Health profile onboarding and redirect flow
- `/plan/` → Personalized plan page
- `/log/` → Log daily activity
- `/progress/` → Progress analytics dashboard
- `/history/` → User log history
- `/chatbot/` → Chat interface page
- `/chatbot-response/` → Chatbot response endpoint
- `/logout/` → Logout action

## 🚀 Installation

### Prerequisites

- Python 3.9+
- pip
- virtual environment support

### Setup

1. Clone the repository

```bash
git clone <repository-url>
cd aromi
```

2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply database migrations

```bash
python manage.py migrate
```

## ▶️ Running the Project

Start the development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## 👤 Default Admin

The project uses Django's built-in admin interface.

Create a superuser if needed:

```bash
python manage.py createsuperuser
```

## 📝 Notes

- The project currently uses SQLite for development.
- Static assets are served from `wellness_app/static`.
- Templates are resolved from the project-level `templates` directory and app templates.
- The chatbot currently uses a keyword-based response system rather than an external AI API.

## 💡 Recommended Next Improvements

- connect the chatbot to an LLM API such as OpenAI or Azure OpenAI
- add password reset and email verification
- add notifications and reminders for logging habits
- add export of progress data to CSV/PDF
- add a real recommendation engine for workout and meal plans

## 📜 License

This project does not currently declare a license file. Add one if you plan to distribute or publish it publicly.
