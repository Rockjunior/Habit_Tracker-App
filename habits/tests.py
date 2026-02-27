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
        """Test creating a new habit."""
        habit = Habit.objects.create(
            task="Test habit",
            periodicity="daily"
        )
        assert habit.task == "Test habit"
        assert habit.periodicity == "daily"
        assert habit.is_active is True
        assert habit.created_at is not None
    
    def test_habit_string_representation(self):
        """Test the string representation of a habit."""
        habit = Habit.objects.create(
            task="Exercise",
            periodicity="daily"
        )
        assert str(habit) == "Exercise (daily)"
    
    def test_complete_task(self):
        """Test completing a habit task."""
        habit = Habit.objects.create(
            task="Read",
            periodicity="daily"
        )
        completion = habit.complete_task()
        
        assert isinstance(completion, HabitCompletion)
        assert completion.habit == habit
        assert habit.completions.count() == 1
    
    def test_is_completed_today_daily(self):
        """Test checking if a daily habit is completed today."""
        habit = Habit.objects.create(
            task="Daily task",
            periodicity="daily"
        )
        
        assert habit.is_completed_today() is False
        
        habit.complete_task()
        assert habit.is_completed_today() is True
    
    def test_get_current_streak_daily(self):
        """Test calculating current streak for daily habits."""
        habit = Habit.objects.create(
            task="Daily habit",
            periodicity="daily"
        )
        
        now = timezone.now()
        
        # Create completions for last 3 days
        for i in range(3):
            date = now - timedelta(days=i)
            habit.complete_task(date)
        
        streak = habit.get_current_streak()
        assert streak == 3
    
    def test_get_current_streak_with_break(self):
        """Test that streak breaks when a day is missed."""
        habit = Habit.objects.create(
            task="Daily habit",
            periodicity="daily"
        )
        
        now = timezone.now()
        
        # Complete today and yesterday
        habit.complete_task(now)
        habit.complete_task(now - timedelta(days=1))
        
        # Skip day 2, complete day 3
        habit.complete_task(now - timedelta(days=3))
        
        streak = habit.get_current_streak()
        assert streak == 2  # Should only count the most recent consecutive days
    
    def test_get_longest_streak(self):
        """Test calculating the longest streak."""
        habit = Habit.objects.create(
            task="Daily habit",
            periodicity="daily",
            created_at=timezone.now() - timedelta(days=20)
        )
        
        now = timezone.now()
        
        # Create a streak of 5 days
        for i in range(5):
            habit.complete_task(now - timedelta(days=i))
        
        # Skip 3 days
        
        # Create earlier streak of 7 days
        for i in range(7):
            habit.complete_task(now - timedelta(days=8 + i))
        
        longest = habit.get_longest_streak()
        assert longest == 7
    
    def test_weekly_habit_streak(self):
        """Test streak calculation for weekly habits."""
        habit = Habit.objects.create(
            task="Weekly habit",
            periodicity="weekly",
            created_at=timezone.now() - timedelta(weeks=5)
        )
        
        now = timezone.now()
        
        # Complete for last 3 weeks
        for i in range(3):
            date = now - timedelta(weeks=i)
            habit.complete_task(date)
        
        streak = habit.get_current_streak()
        assert streak == 3


@pytest.mark.django_db
class TestHabitCompletion:
    """Test cases for the HabitCompletion model."""
    
    def test_create_completion(self):
        """Test creating a habit completion."""
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
        """Test the string representation of a completion."""
        habit = Habit.objects.create(task="Test", periodicity="daily")
        completion = HabitCompletion.objects.create(habit=habit)
        
        assert "Test completed at" in str(completion)


@pytest.mark.django_db
class TestAnalytics:
    """Test cases for the analytics module (functional programming)."""
    
    def test_get_all_habits(self):
        """Test retrieving all active habits."""
        Habit.objects.create(task="Habit 1", periodicity="daily")
        Habit.objects.create(task="Habit 2", periodicity="weekly")
        Habit.objects.create(task="Inactive", periodicity="daily", is_active=False)
        
        habits = Habit.objects.all()
        result = analytics.get_all_habits(habits)
        
        assert len(result) == 2
        assert all('task' in h for h in result)
        assert all('current_streak' in h for h in result)
    
    def test_get_habits_by_periodicity(self):
        """Test filtering habits by periodicity."""
        Habit.objects.create(task="Daily 1", periodicity="daily")
        Habit.objects.create(task="Daily 2", periodicity="daily")
        Habit.objects.create(task="Weekly 1", periodicity="weekly")
        
        habits = Habit.objects.all()
        daily = analytics.get_habits_by_periodicity(habits, "daily")
        weekly = analytics.get_habits_by_periodicity(habits, "weekly")
        
        assert len(daily) == 2
        assert len(weekly) == 1
    
    def test_get_longest_streak_all_habits(self):
        """Test finding the longest streak across all habits."""
        habit1 = Habit.objects.create(task="Habit 1", periodicity="daily")
        habit2 = Habit.objects.create(task="Habit 2", periodicity="daily")
        
        now = timezone.now()
        
        # Habit 1: streak of 3
        for i in range(3):
            habit1.complete_task(now - timedelta(days=i))
        
        # Habit 2: streak of 5
        for i in range(5):
            habit2.complete_task(now - timedelta(days=i))
        
        habits = Habit.objects.all()
        result = analytics.get_longest_streak_all_habits(habits)
        
        assert result['streak'] == 5
        assert result['habit']['task'] == "Habit 2"
    
    def test_get_completion_stats(self):
        """Test calculating comprehensive statistics."""
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
        """Test identifying habits with low streaks."""
        habit1 = Habit.objects.create(task="Struggling", periodicity="daily")
        habit2 = Habit.objects.create(task="Good", periodicity="daily")
        
        now = timezone.now()
        
        # Habit 2 has good streak
        for i in range(5):
            habit2.complete_task(now - timedelta(days=i))
        
        habits = Habit.objects.all()
        struggling = analytics.get_struggling_habits(habits)
        
        assert len(struggling) == 1
        assert struggling[0]['task'] == "Struggling"
    
    def test_calculate_completion_rate(self):
        """Test calculating completion rate for a habit."""
        habit = Habit.objects.create(task="Test", periodicity="daily")
        
        now = timezone.now()
        
        # Complete 15 out of last 30 days
        for i in range(0, 30, 2):  # Every other day
            habit.complete_task(now - timedelta(days=i))
        
        rate = analytics.calculate_completion_rate(habit, days=30)
        
        assert 0 <= rate <= 100
        assert rate > 40  # At least 40% (15/30 = 50%)


@pytest.mark.django_db
class TestViews:
    """Test cases for views."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = Client()
    
    def test_home_view(self):
        """Test the home page view."""
        response = self.client.get(reverse('home'))
        
        assert response.status_code == 200
        assert 'habits' in response.context
        assert 'stats' in response.context
    
    def test_habit_list_view(self):
        """Test the habit list view."""
        Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('habit_list'))
        
        assert response.status_code == 200
        assert 'habits' in response.context
    
    def test_add_habit_view_get(self):
        """Test GET request to add habit page."""
        response = self.client.get(reverse('add_habit'))
        
        assert response.status_code == 200
    
    def test_add_habit_view_post(self):
        """Test POST request to create a new habit."""
        data = {
            'task': 'New Habit',
            'periodicity': 'daily'
        }
        
        response = self.client.post(reverse('add_habit'), data)
        
        assert response.status_code == 302  # Redirect after success
        assert Habit.objects.filter(task='New Habit').exists()
    
    def test_habit_detail_view(self):
        """Test the habit detail view."""
        habit = Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('habit_detail', args=[habit.id]))
        
        assert response.status_code == 200
        assert response.context['habit'] == habit
    
    def test_complete_habit_view(self):
        """Test completing a habit via view."""
        habit = Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('complete_habit', args=[habit.id]))
        
        assert response.status_code == 302  # Redirect after completion
        assert habit.completions.count() == 1
    
    def test_analytics_view(self):
        """Test the analytics dashboard view."""
        Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('analytics'))
        
        assert response.status_code == 200
        assert 'stats' in response.context
        assert 'all_habits' in response.context
    
    def test_api_habit_list(self):
        """Test the API endpoint for habit list."""
        Habit.objects.create(task="Test", periodicity="daily")
        
        response = self.client.get(reverse('api_habit_list'))
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data['success'] is True
        assert 'habits' in json_data
    
    def test_api_analytics(self):
        """Test the API endpoint for analytics."""
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
        """Test habit creation with default values."""
        habit = Habit.objects.create(task="Test")
        
        self.assertEqual(habit.periodicity, "daily")
        self.assertTrue(habit.is_active)
    
    def test_habit_ordering(self):
        """Test that habits are ordered by creation date (newest first)."""
        old_habit = Habit.objects.create(
            task="Old",
            created_at=timezone.now() - timedelta(days=5)
        )
        new_habit = Habit.objects.create(task="New")
        
        habits = list(Habit.objects.all())
        self.assertEqual(habits[0], new_habit)
        self.assertEqual(habits[1], old_habit)
