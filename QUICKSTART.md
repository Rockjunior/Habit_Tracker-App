# Quick Start: Habit Tracker

Get the app running using the following steps.

## 1) Install and set up

```bash
# Open the project folder
cd Habit_Tracker-App

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database tables
python manage.py migrate

# Optional (recommended): load sample habits and history
python manage.py populate_habits
```

## 2) Start the app

```bash
python manage.py runserver
```

Open your browser at: http://127.0.0.1:8000/

---

## First things to try

### Create your first habit

1. Click **Add New Habit**
2. Enter a name (example: "Exercise 30 minutes")
3. Choose **Daily** or **Weekly**
4. Click **Create Habit**

### Mark a habit as done

- From the home page: click **Mark Complete**
- From the habit detail page: click **Mark as Complete**

### Check your progress

- **Home**: quick overview of habits and streaks
- **Analytics**: best performers, weak spots, grouped stats
- **Habit detail**: current streak, longest streak, recent completions

---

## How streaks work

### Daily habits

- Complete at least once per day to keep your streak
- Miss a day and the streak resets

### Weekly habits

- Complete at least once per week to keep your streak
- Miss a week and the streak resets
- Weeks start on Monday

### Simple example (daily)

- Mon: ✅
- Tue: ❌
- Wed: ✅
- Result: **1-day streak** (restarted)

---

## Run tests

```bash
# Run all tests
pytest

# Verbose output
pytest -v
```

You should see all **27 tests** passing.

---

## Sample data included

`python manage.py populate_habits` creates 5 habits with realistic 4-week history:

1. **Drink 8 glasses of water** (Daily)
2. **Exercise for 30 minutes** (Daily)
3. **Read a book for 20 minutes** (Daily)
4. **Attend yoga class** (Weekly)
5. **Grocery shopping** (Weekly)

---

## Common tasks

### View all habits

Go to **My Habits** in the menu.

### Filter habits

Use the periodicity dropdown on the **My Habits** page.

### Delete a habit

1. Open the habit detail page
2. Click **Delete Habit**
3. Confirm

### Access Django admin

1. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
2. Open: http://127.0.0.1:8000/admin/
3. Sign in with your superuser account

---

## API quick access

### All habits (JSON)

```http
GET http://127.0.0.1:8000/api/habits/
```

### Analytics (JSON)

```http
GET http://127.0.0.1:8000/api/analytics/
```

---

## Troubleshooting

### Database reset

```bash
# If needed, delete db.sqlite3 first
python manage.py migrate
python manage.py populate_habits
```

### Virtual environment issues

```bash
deactivate
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Server won’t start on port 8000

```bash
python manage.py runserver 8080
```

---

## Need more detail?

- Full docs: [README.md](README.md)
- Usage examples: check test files
- Questions/issues: open a GitHub issue

---

Happy tracking! 🎯
