# Habit Tracker Application

A comprehensive Django-based habit tracking application built with Python, demonstrating Object-Oriented Programming (OOP) principles and Functional Programming paradigms.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Assignment Requirements](#assignment-requirements)

## 🎯 Overview

The Habit Tracker Application allows users to define, track, and analyze their habits. Users can create habits with specific periodicities (daily or weekly), mark them as complete, and view comprehensive analytics about their progress including streak calculations and completion rates.

This project was developed as part of the **DLBDSOOFPP01** (Object-Oriented and Functional Programming with Python) portfolio assignment.

## ✨ Features

### Core Functionality

- **Habit Management**
  - Create new habits with customizable tasks and periodicities (daily/weekly)
  - View all active habits in an organized dashboard
  - Mark habits as complete for the current period
  - Delete (deactivate) habits when no longer needed
  
- **Streak Tracking**
  - Automatic calculation of current streaks
  - Track longest streak achieved for each habit
  - Visual indicators for habit completion status
  
- **Analytics Dashboard**
  - View all habits grouped by periodicity
  - Identify best-performing habits
  - Detect struggling habits that need attention
  - Calculate completion rates over custom periods
  - Find the longest streak across all habits
  
- **Data Persistence**
  - All data stored in SQLite database
  - Django ORM for database interactions
  - Migrations for schema management

### Technical Features

- **Object-Oriented Design**
  - `Habit` class with comprehensive methods
  - `HabitCompletion` class for tracking completions
  - Proper encapsulation and abstraction
  
- **Functional Programming**
  - Dedicated analytics module using functional paradigms
  - Extensive use of `map()`, `filter()`, and `reduce()`
  - Pure functions for data analysis
  
- **Web Interface**
  - Clean, modern Bootstrap-based UI
  - Responsive design for mobile and desktop
  - RESTful API endpoints for programmatic access

## 🏗️ Technical Architecture

### Object-Oriented Programming (OOP)

The application uses OOP principles throughout:

**`Habit` Model:**
- Attributes: `task`, `periodicity`, `created_at`, `is_active`
- Methods:
  - `complete_task()` - Mark habit as completed
  - `get_current_streak()` - Calculate current consecutive streak
  - `get_longest_streak()` - Find longest streak ever achieved
  - `is_completed_today()` - Check if completed in current period
  - `_get_period_start()` - Internal helper for period calculations

**`HabitCompletion` Model:**
- Tracks individual completion events
- Related to Habit via foreign key
- Automatic timestamp on creation

### Functional Programming

The `analytics.py` module demonstrates functional programming:

```python
# Example: Using map, filter, and reduce
habits_with_streaks = list(map(
    lambda habit: {
        'habit': habit,
        'streak': habit.get_longest_streak()
    },
    habits_queryset
))

best_habit = reduce(
    lambda max_item, current_item: 
        current_item if current_item['streak'] > max_item['streak'] 
        else max_item,
    habits_with_streaks
)
```

Functions include:
- `get_all_habits()` - Retrieve all active habits
- `get_habits_by_periodicity()` - Filter by periodicity
- `get_longest_streak_all_habits()` - Find maximum streak
- `get_completion_stats()` - Calculate comprehensive statistics
- `calculate_completion_rate()` - Percentage completion rate

## 🚀 Installation

### Prerequisites

- Python 3.7 or later
- pip (Python package manager)
- Git (for cloning the repository)

### Step-by-Step Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/Habit_Tracker-App.git
   cd Habit_Tracker-App
   ```

2. **Create and activate a virtual environment:**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Populate with sample data (optional but recommended):**
   ```bash
   python manage.py populate_habits
   ```
   
   This creates 5 predefined habits with 4 weeks of realistic tracking data.

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📖 Usage

### Creating a New Habit

1. Navigate to the home page
2. Click "Add New Habit" or go to the "Add Habit" page
3. Enter the habit description (e.g., "Exercise for 30 minutes")
4. Select the periodicity (Daily or Weekly)
5. Click "Create Habit"

### Completing a Habit

**From the Home Page:**
1. Find your habit in the list
2. Click "Mark Complete"
3. Confirmation message will appear

**From Habit Detail Page:**
1. Click on a habit to view details
2. Click "Mark as Complete"
3. The habit will be marked for the current period

### Viewing Analytics

1. Click "Analytics" in the navigation menu
2. View comprehensive statistics:
   - Overall statistics (total habits, completions, average streak)
   - Longest streak achievement across all habits
   - Best performing habits
   - Habits grouped by periodicity
   - Habits needing attention (low streaks)

### Managing Habits

**View Habit Details:**
- Click on any habit name or "View Details"
- See current streak, longest streak, and completion rate
- View recent completions (last 30 days)

**Delete a Habit:**
- Go to habit detail page
- Click "Delete Habit"
- Confirm deletion (habit will be deactivated, not permanently removed)

## 🧪 Testing

The application includes a comprehensive test suite with 27 unit tests.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest habits/tests.py

# Run with coverage report
pytest --cov=habits --cov-report=html
```

### Test Coverage

Tests cover:
- **Model Tests** (Habit and HabitCompletion)
  - Creation, validation, and string representation
  - Streak calculation logic (daily and weekly)
  - Completion tracking
  
- **Analytics Tests**
  - Functional programming functions
  - Filtering and aggregation
  - Statistical calculations
  
- **View Tests**
  - All page views (home, list, detail, add, analytics)
  - Form submissions
  - API endpoints

All tests pass successfully:
```
============================= 27 passed in 0.60s ==============================
```

## 📁 Project Structure

```
Habit_Tracker-App/
│
├── habits/                          # Main Django app
│   ├── management/
│   │   └── commands/
│   │       └── populate_habits.py  # Command to populate sample data
│   ├── migrations/                 # Database migrations
│   ├── templates/
│   │   └── habits/                 # HTML templates
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── habit_list.html
│   │       ├── habit_detail.html
│   │       ├── add_habit.html
│   │       ├── analytics.html
│   │       └── delete_habit.html
│   ├── admin.py                    # Admin interface configuration
│   ├── analytics.py                # Functional programming analytics module
│   ├── apps.py                     # App configuration
│   ├── models.py                   # OOP models (Habit, HabitCompletion)
│   ├── tests.py                    # Comprehensive test suite
│   ├── urls.py                     # URL routing
│   └── views.py                    # View functions
│
├── habit_tracker_project/          # Django project settings
│   ├── settings.py                 # Project configuration
│   ├── urls.py                     # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── venv/                           # Virtual environment (not in git)
├── db.sqlite3                      # SQLite database (not in git)
├── manage.py                       # Django management script
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🔌 API Documentation

The application provides RESTful API endpoints for programmatic access.

### Endpoints

#### Get All Habits
```
GET /api/habits/
```

**Response:**
```json
{
  "success": true,
  "habits": [
    {
      "id": 1,
      "task": "Exercise for 30 minutes",
      "periodicity": "daily",
      "created_at": "2026-01-27T10:00:00Z",
      "is_active": true,
      "current_streak": 5
    }
  ],
  "count": 1
}
```

#### Get Analytics
```
GET /api/analytics/
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_habits": 5,
    "daily_habits": 3,
    "weekly_habits": 2,
    "total_completions": 72,
    "average_streak": 3.4
  },
  "longest_streak": {
    "habit": {
      "id": 3,
      "task": "Read a book",
      "periodicity": "daily"
    },
    "streak": 11
  },
  "best_performers": [...]
}
```

## 👨‍💻 Development

### Adding New Features

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

3. **Run tests:**
   ```bash
   pytest
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

### Database Management

**Create new migration:**
```bash
python manage.py makemigrations
```

**Apply migrations:**
```bash
python manage.py migrate
```

**Reset database:**
```bash
# Delete db.sqlite3
python manage.py migrate
python manage.py populate_habits
```

## 📝 Assignment Requirements Checklist

This project meets all requirements of the DLBDSOOFPP01 assignment:

- ✅ **Python 3.7+**: Using Python 3.13
- ✅ **OOP Implementation**: Habit and HabitCompletion classes with methods
- ✅ **Data Persistence**: SQLite database with Django ORM
- ✅ **Analytics Module**: Functional programming in `analytics.py`
- ✅ **User Interface**: Django web interface with Bootstrap
- ✅ **Testing**: 27 unit tests using pytest
- ✅ **Habit Management**: Create, complete, delete habits
- ✅ **Periodicities**: Daily and weekly supported
- ✅ **Streak Tracking**: Current and longest streaks calculated
- ✅ **5 Predefined Habits**: Populated via management command
- ✅ **4 Weeks of Data**: Sample data with realistic completions
- ✅ **Analytics Functions**:
  - ✅ List all tracked habits
  - ✅ List habits by periodicity
  - ✅ Longest streak across all habits
  - ✅ Longest streak for specific habit
- ✅ **Documentation**: Comprehensive README with docstrings
- ✅ **Code Quality**: Well-structured, commented, and documented

## 📄 License

This project is created for educational purposes as part of the DLBDSOOFPP01 course.

## 👤 Author

Created as part of the Object-Oriented and Functional Programming with Python portfolio assignment.

## 🙏 Acknowledgments

- Django framework for rapid web development
- Bootstrap for responsive UI design
- pytest for comprehensive testing capabilities
- The DLBDSOOFPP01 course instructors for project requirements

---

**GitHub Repository:** https://github.com/<your-username>/Habit_Tracker-App

For questions or issues, please open an issue on GitHub.