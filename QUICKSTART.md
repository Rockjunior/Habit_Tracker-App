# Quick Start Guide - Habit Tracker Application

## Installation & Setup (5 minutes)

### 1. Install the Application

```bash
# Clone or navigate to the project
cd Habit_Tracker-App

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Load sample data
python manage.py populate_habits
```

### 2. Run the Application

```bash
python manage.py runserver
```

Open your browser and go to: http://127.0.0.1:8000/

## Quick Usage Guide

### Creating Your First Habit

1. Click **"Add New Habit"** button
2. Enter habit name (e.g., "Exercise 30 minutes")
3. Choose periodicity: **Daily** or **Weekly**
4. Click **"Create Habit"**

### Completing a Habit

**Option 1 - From Home Page:**
- Find your habit
- Click **"Mark Complete"** button

**Option 2 - From Habit Details:**
- Click on habit name
- Click **"Mark as Complete"**

### Viewing Your Progress

**Home Dashboard:**
- See all habits with current streaks
- View statistics (total habits, completions, average streak)
- Identify best performers and struggling habits

**Analytics Page:**
- Comprehensive statistics
- Longest streaks across all habits
- Habits grouped by periodicity (daily/weekly)
- Best performing habits
- Habits needing attention

**Individual Habit Details:**
- Current streak
- Longest streak ever achieved
- 30-day completion rate
- Recent completion history

## Testing the Application

```bash
# Run all tests
pytest

# Run with detailed output
pytest -v

# All 27 tests should pass
```

## Understanding Streaks

### Daily Habits
- Complete at least once per day to maintain streak
- Missing a day breaks the streak
- Streak resets to 0 if you miss a period

### Weekly Habits
- Complete at least once per week to maintain streak
- Missing a week breaks the streak
- Week starts on Monday

### Streak Examples

**Good Streak (Daily):**
- Monday: ✓ Completed
- Tuesday: ✓ Completed
- Wednesday: ✓ Completed
- **Result:** 3-day streak

**Broken Streak (Daily):**
- Monday: ✓ Completed
- Tuesday: ✗ Missed
- Wednesday: ✓ Completed
- **Result:** 1-day streak (restarted)

## Sample Data

The `populate_habits` command creates 5 habits:

1. **Drink 8 glasses of water** (Daily) - 85% completion rate
2. **Exercise for 30 minutes** (Daily) - 70% completion rate
3. **Read a book for 20 minutes** (Daily) - 60% completion rate
4. **Attend yoga class** (Weekly) - 75% completion rate
5. **Grocery shopping** (Weekly) - 90% completion rate

Each habit has 4 weeks of realistic tracking data with varying streaks.

## Common Tasks

### View All Habits
Navigate to: **My Habits** in the menu

### Filter Habits
On "My Habits" page, use the periodicity dropdown filter

### Delete a Habit
1. Go to habit detail page
2. Click "Delete Habit"
3. Confirm deletion

### Access Admin Panel
1. Create superuser: `python manage.py createsuperuser`
2. Visit: http://127.0.0.1:8000/admin/
3. Login with superuser credentials

## API Access

### Get All Habits (JSON)
```
GET http://127.0.0.1:8000/api/habits/
```

### Get Analytics (JSON)
```
GET http://127.0.0.1:8000/api/analytics/
```

## Tips for Success

1. **Start Small:** Begin with 2-3 habits you can realistically maintain
2. **Be Consistent:** Complete habits at the same time each day
3. **Review Analytics:** Check your analytics weekly to stay motivated
4. **Adjust Goals:** If you're struggling with a habit, consider changing its periodicity
5. **Celebrate Wins:** Acknowledge your longest streaks and progress

## Troubleshooting

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py populate_habits
```

### Virtual Environment Issues
```bash
# Deactivate and reactivate
deactivate
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Server Not Starting
```bash
# Check if port 8000 is in use
# Try a different port
python manage.py runserver 8080
```

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review test files for usage examples
- Open an issue on GitHub

---

**Enjoy tracking your habits and building better routines!** 🎯