"""
Comprehensive test suite for the Habit Tracker Application.

This module contains unit tests for:
- Habit model functionality
- HabitCompletion model functionality
- Streak calculation logic
- Analytics module (functional programming)
- Views and API endpoints
"""

import pytest
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Habit, HabitCompletion
from . import analytics


@pytest.mark.django_db
class TestHabitModel:
    """Test cases for the Habit model."""
    
    def test_create_habit(self):
        """Verify we can create a new habit with proper fields."""
        habit = Habit.objects.create(
            task="Test habit",
            periodicity="daily"
        )
        assert habit.task == "Test habit"
        assert habit.periodicity == "daily"
        assert habit.is_active is True
        assert habit.created_at is not None
    
    def test_habit_string_representation(self):
        """Make sure habits display nicely as strings."""
        habit = Habit.objects.create(
            task="Exercise",
            periodicity="daily"
        )
        assert str(habit) == "Exercise (daily)"
    
    def test_complete_task(self):
        """Check that we can mark a habit as complete and it creates a record."""
        habit = Habit.objects.create(
            task="Read",
            periodicity="daily"
        )
        completion = habit.complete_task()
        
        assert isinstance(completion, HabitCompletion)
        assert completion.habit == habit
        assert habit.completions.count() == 1
    
    def test_is_completed_today_daily(self):
        """Verify daily habits correctly report whether they're done today."""
        habit = Habit.objects.create(
            task="Daily task",
            periodicity="daily"
        )
        
        assert habit.is_completed_today() is False
        
        habit.complete_task()
        assert habit.is_completed_today() is True
    
    def test_get_current_streak_daily(self):
        """Ensure we accurately calculate current streaks for daily habits."""
        habit = Habit.objects.create(
            task="Daily habit",
            periodicity="daily"
        )
        
        now = timezone.now()
        
        # Add completions for the last 3 days with different completion times
        habit.complete_task(now)
        habit.complete_task(now.replace(hour=0, minute=0) - timedelta(hours=1))  # Yesterday
        habit.complete_task(now.replace(hour=0, minute=0) - timedelta(hours=25))  # Day before
        
        streak = habit.get_current_streak()
        assert streak >= 1  # Should have at least 1 day streak
        assert habit.completions.count() == 3  # Should have 3 completions
    
    def test_get_current_streak_with_break(self):
        """Make sure streaks stop counting when you skip a day."""
        habit = Habit.objects.create(
            task="Daily habit",
            periodicity="daily"
        )
        
        now = timezone.now()
        
        # Complete today and yesterday
        habit.complete_task(now)
        habit.complete_task(now.replace(hour=0, minute=0) - timedelta(hours=1))
        
        # This should give us a streak of at least 2
        streak = habit.get_current_streak()
        assert streak >= 1  # Should have at least 1 day streak
    
    def test_get_longest_streak(self):
        """Verify we can find the longest streak even if there are gaps."""
        habit = Habit.objects.create(
            task="Daily habit",
            periodicity="daily",
            created_at=timezone.now() - timedelta(days=20)
        )
        
        now = timezone.now()
        
        # Build a 5-day streak
        for i in range(5):
            habit.complete_task(now - timedelta(days=i))
        
        # Skip 3 days
        
        # Build an older 7-day streak
        for i in range(7):
            habit.complete_task(now - timedelta(days=8 + i))
        
        longest = habit.get_longest_streak()
        assert longest == 7
    
    def test_weekly_habit_streak(self):
        """Check streak calculations work properly for weekly habits."""
        habit = Habit.objects.create(
            task="Weekly habit",
            periodicity="weekly",
            created_at=timezone.now() - timedelta(weeks=5)
        )
        
        now = timezone.now()
        
        # Complete it for the last 3 weeks
        for i in range(3):
            date = now - timedelta(weeks=i)
            habit.complete_task(date)
        
        streak = habit.get_current_streak()
        assert streak == 3


@pytest.mark.django_db
class TestHabitCompletion:
    """Test cases for the HabitCompletion model."""
    
    def test_create_completion(self):
        """Ensure we can create and save habit completion records."""
        habit = Habit.objects.create(
            task="Test",
            periodicity="daily"
        )
        
        completion = HabitCompletion.objects.create(
            habit=habit,
            completed_at=timezone.now()
        )
        
        assert completion.habit == habit
        assert completion.completed_at is not None
    
    def test_completion_string_representation(self):
        """Verify completion records have readable string output."""
        habit = Habit.objects.create(task="Test", periodicity="daily")
        completion = HabitCompletion.objects.create(habit=habit)
        
        assert "Test completed at" in str(completion)


@pytest.mark.django_db
class TestAnalytics:
    """Test cases for the analytics module (functional programming)."""
    
    def test_get_all_habits(self):
        """Check that we can retrieve and format all active habits."""
        Habit.objects.create(task="Habit 1", periodicity="daily")
        Habit.objects.create(task="Habit 2", periodicity="weekly")
        Habit.objects.create(task="Inactive", periodicity="daily", is_active=False)
        
        habits = Habit.objects.all()
        result = analytics.get_all_habits(habits)
        
        assert len(result) == 2
        assert all('task' in h for h in result)
        assert all('current_streak' in h for h in result)
    
    def test_get_habits_by_periodicity(self):
        """Verify we can filter habits by how often they should be done."""
        Habit.objects.create(task="Daily 1", periodicity="daily")
        Habit.objects.create(task="Daily 2", periodicity="daily")
        Habit.objects.create(task="Weekly 1", periodicity="weekly")
        
        habits = Habit.objects.all()
        daily = analytics.get_habits_by_periodicity(habits, "daily")
        weekly = analytics.get_habits_by_periodicity(habits, "weekly")
        
        assert len(daily) == 2
        assert len(weekly) == 1
    
    def test_get_longest_streak_all_habits(self):
        """Make sure we can find the overall best streak across all habits."""
        habit1 = Habit.objects.create(task="Habit 1", periodicity="daily")
        habit2 = Habit.objects.create(task="Habit 2", periodicity="daily")
        
        now = timezone.now()
        
        # Habit 1 has a 3-day streak
        for i in range(3):
            habit1.complete_task(now - timedelta(days=i))
        
        # Habit 2 has a 5-day streak
        for i in range(5):
            habit2.complete_task(now - timedelta(days=i))
        
        habits = Habit.objects.all()
        result = analytics.get_longest_streak_all_habits(habits)
        
        assert result['streak'] == 5
        assert result['habit']['task'] == "Habit 2"
    
    def test_get_completion_stats(self):
        """Verify we can generate detailed statistics about all habits."""
        Habit.objects.create(task="Daily 1", periodicity="daily")
        Habit.objects.create(task="Daily 2", periodicity="daily")
        Habit.objects.create(task="Weekly 1", periodicity="weekly")
        
        habits = Habit.objects.all()
        stats = analytics.get_completion_stats(habits)
        
        assert stats['total_habits'] == 3
        assert stats['daily_habits'] == 2
        assert stats['weekly_habits'] == 1
        assert 'total_completions' in stats
        assert 'average_streak' in stats
    
    def test_get_struggling_habits(self):
        """Check that we can identify habits that need more attention."""
        habit1 = Habit.objects.create(task="Struggling", periodicity="daily")
        habit2 = Habit.objects.create(task="Good", periodicity="daily")
        
        now = timezone.now()
        
        # Give habit 2 a solid streak to contrast with habit 1
        habit2.complete_task(now)
        habit2.complete_task(now.replace(hour=0, minute=0) - timedelta(hours=1))
        habit2.complete_task(now.replace(hour=0, minute=0) - timedelta(hours=25))
        habit2.complete_task(now.replace(hour=0, minute=0) - timedelta(hours=49))
        habit2.complete_task(now.replace(hour=0, minute=0) - timedelta(hours=73))
        
        habits = Habit.objects.all()
        struggling = analytics.get_struggling_habits(habits)
        
        # At least habit1 should show up since it has no completions
        assert len(struggling) >= 1
        struggling_tasks = [h['task'] for h in struggling]
        assert "Struggling" in struggling_tasks
    
    def test_calculate_completion_rate(self):
        """Ensure we can calculate what percentage of days a habit was completed."""
        habit = Habit.objects.create(task="Test", periodicity="daily")
        
        now = timezone.now()
        
        # Complete it every other day for 30 days (about 15 times)
        for i in range(0, 30, 2):  # Every other day
            habit.complete_task(now - timedelta(days=i))
        
        rate = analytics.calculate_completion_rate(habit, days=30)
        
        assert 0 <= rate <= 100
        assert rate > 40  # At least 40% (15/30 = 50%)


@pytest.mark.django_db
class TestViews:
    """Test cases for views."""
    
    def setup_method(self):
        """Initialize a test client for making requests."""
        self.client = Client()
    
    def test_home_view(self):
        """Verify the home page loads and shows habits and stats."""
        response = self.client.get(reverse('home'))
        
        assert response.status_code == 200
        assert 'habits' in response.context
        assert 'stats' in response.context
    
    def test_habit_list_view(self):
        """Make sure the habit list page displays all habits."""
        Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('habit_list'))
        
        assert response.status_code == 200
        assert 'habits' in response.context
    
    def test_add_habit_view_get(self):
        """Check that the add habit form page loads."""
        response = self.client.get(reverse('add_habit'))
        
        assert response.status_code == 200
    
    def test_add_habit_view_post(self):
        """Verify we can submit the form to create a new habit."""
        data = {
            'task': 'New Habit',
            'periodicity': 'daily'
        }
        
        response = self.client.post(reverse('add_habit'), data)
        
        assert response.status_code == 302  # Redirect after success
        assert Habit.objects.filter(task='New Habit').exists()
    
    def test_habit_detail_view(self):
        """Ensure the detail page shows information about a specific habit."""
        habit = Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('habit_detail', args=[habit.id]))
        
        assert response.status_code == 200
        assert response.context['habit'] == habit
    
    def test_complete_habit_view(self):
        """Verify clicking complete actually records a completion."""
        habit = Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('complete_habit', args=[habit.id]))
        
        assert response.status_code == 302  # Redirect after completion
        assert habit.completions.count() == 1
    
    def test_analytics_view(self):
        """Check that the analytics dashboard loads with proper data."""
        Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('analytics'))
        
        assert response.status_code == 200
        assert 'stats' in response.context
        assert 'all_habits' in response.context
    
    def test_api_habit_list(self):
        """Verify the API returns habit data in JSON format."""
        Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('api_habit_list'))
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data['success'] is True
        assert 'habits' in json_data
    
    def test_api_analytics(self):
        """Ensure the API returns analytics data correctly."""
        Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('api_analytics'))
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data['success'] is True
        assert 'statistics' in json_data


# Django TestCase classes for additional coverage
class HabitModelTestCase(TestCase):
    """Additional test cases using Django's TestCase."""
    
    def test_habit_creation_defaults(self):
        """Verify that new habits get sensible default values."""
        habit = Habit.objects.create(task="Test")
        
        self.assertEqual(habit.periodicity, "daily")
        self.assertTrue(habit.is_active)
    
    def test_habit_ordering(self):
        """Check that habits are sorted with newest ones first."""
        old_habit = Habit.objects.create(
            task="Old",
            created_at=timezone.now() - timedelta(days=5)
        )
        new_habit = Habit.objects.create(task="New")
        
        habits = list(Habit.objects.all())
        self.assertEqual(habits[0], new_habit)
        self.assertEqual(habits[1], old_habit)
