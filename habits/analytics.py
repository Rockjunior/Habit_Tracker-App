"""
Analytics module for Habit Tracker Application.

This module uses functional programming paradigms to analyze habit data.
It provides functions to calculate statistics and insights about habits
and their completion patterns.
"""

from typing import List, Dict, Optional, Callable
from functools import reduce
from datetime import datetime, timedelta
from django.db.models import QuerySet


def get_all_habits(habits_queryset: QuerySet) -> List[Dict]:
    """
    Return a list of all currently tracked habits.
    
    Args:
        habits_queryset: QuerySet of Habit objects
    
    Returns:
        List of dictionaries containing habit information
    """
    return list(map(
        lambda habit: {
            'id': habit.id,
            'task': habit.task,
            'periodicity': habit.periodicity,
            'created_at': habit.created_at,
            'is_active': habit.is_active,
            'current_streak': habit.get_current_streak(),
        },
        filter(lambda h: h.is_active, habits_queryset)
    ))


def get_habits_by_periodicity(habits_queryset: QuerySet, periodicity: str) -> List[Dict]:
    """
    Return a list of all habits with the specified periodicity.
    
    Args:
        habits_queryset: QuerySet of Habit objects
        periodicity: The periodicity to filter by ('daily' or 'weekly')
    
    Returns:
        List of dictionaries containing habit information
    """
    filtered_habits = filter(
        lambda h: h.is_active and h.periodicity == periodicity,
        habits_queryset
    )
    
    return list(map(
        lambda habit: {
            'id': habit.id,
            'task': habit.task,
            'periodicity': habit.periodicity,
            'created_at': habit.created_at,
            'current_streak': habit.get_current_streak(),
        },
        filtered_habits
    ))


def get_longest_streak_all_habits(habits_queryset: QuerySet) -> Dict:
    """
    Return the longest streak across all habits.
    
    Args:
        habits_queryset: QuerySet of Habit objects
    
    Returns:
        Dictionary containing the habit with the longest streak and the streak count
    """
    if not habits_queryset.exists():
        return {'habit': None, 'streak': 0}
    
    # Map each habit to its longest streak
    habit_streaks = list(map(
        lambda habit: {
            'habit': habit,
            'streak': habit.get_longest_streak()
        },
        habits_queryset
    ))
    
    # Reduce to find the maximum streak
    max_streak_info = reduce(
        lambda max_item, current_item: current_item if current_item['streak'] > max_item['streak'] else max_item,
        habit_streaks,
        habit_streaks[0]
    )
    
    return {
        'habit': {
            'id': max_streak_info['habit'].id,
            'task': max_streak_info['habit'].task,
            'periodicity': max_streak_info['habit'].periodicity,
        },
        'streak': max_streak_info['streak']
    }


def get_longest_streak_for_habit(habit) -> int:
    """
    Return the longest streak for a specific habit.
    
    Args:
        habit: A Habit object
    
    Returns:
        The longest streak count for the habit
    """
    return habit.get_longest_streak()


def get_current_streaks_all_habits(habits_queryset: QuerySet) -> List[Dict]:
    """
    Return current streaks for all habits.
    
    Args:
        habits_queryset: QuerySet of Habit objects
    
    Returns:
        List of dictionaries containing habit and current streak information
    """
    return list(map(
        lambda habit: {
            'id': habit.id,
            'task': habit.task,
            'periodicity': habit.periodicity,
            'current_streak': habit.get_current_streak(),
        },
        filter(lambda h: h.is_active, habits_queryset)
    ))


def get_completion_stats(habits_queryset: QuerySet) -> Dict:
    """
    Calculate comprehensive statistics about habit completions.
    
    Args:
        habits_queryset: QuerySet of Habit objects
    
    Returns:
        Dictionary containing various statistics
    """
    if not habits_queryset.exists():
        return {
            'total_habits': 0,
            'daily_habits': 0,
            'weekly_habits': 0,
            'total_completions': 0,
            'average_streak': 0,
        }
    
    active_habits = list(filter(lambda h: h.is_active, habits_queryset))
    
    # Count by periodicity
    daily_count = len(list(filter(lambda h: h.periodicity == 'daily', active_habits)))
    weekly_count = len(list(filter(lambda h: h.periodicity == 'weekly', active_habits)))
    
    # Total completions
    total_completions = reduce(
        lambda total, habit: total + habit.completions.count(),
        active_habits,
        0
    )
    
    # Average current streak
    current_streaks = list(map(lambda h: h.get_current_streak(), active_habits))
    average_streak = sum(current_streaks) / len(current_streaks) if current_streaks else 0
    
    return {
        'total_habits': len(active_habits),
        'daily_habits': daily_count,
        'weekly_habits': weekly_count,
        'total_completions': total_completions,
        'average_streak': round(average_streak, 2),
    }


def get_struggling_habits(habits_queryset: QuerySet) -> List[Dict]:
    """
    Identify habits with zero or low current streaks (struggling habits).
    
    Args:
        habits_queryset: QuerySet of Habit objects
    
    Returns:
        List of habits with current streak of 0 or 1
    """
    struggling = filter(
        lambda habit: habit.get_current_streak() <= 1,
        filter(lambda h: h.is_active, habits_queryset)
    )
    
    return list(map(
        lambda habit: {
            'id': habit.id,
            'task': habit.task,
            'periodicity': habit.periodicity,
            'current_streak': habit.get_current_streak(),
        },
        struggling
    ))


def get_habits_completed_in_period(habits_queryset: QuerySet, start_date: datetime, end_date: datetime) -> List[Dict]:
    """
    Get all habits that were completed at least once in the specified period.
    
    Args:
        habits_queryset: QuerySet of Habit objects
        start_date: Start of the period
        end_date: End of the period
    
    Returns:
        List of habits completed in the period with completion count
    """
    def count_completions_in_period(habit):
        count = habit.completions.filter(
            completed_at__gte=start_date,
            completed_at__lte=end_date
        ).count()
        return {
            'id': habit.id,
            'task': habit.task,
            'periodicity': habit.periodicity,
            'completions_in_period': count,
        }
    
    habits_with_completions = map(count_completions_in_period, habits_queryset)
    return list(filter(lambda h: h['completions_in_period'] > 0, habits_with_completions))


def calculate_completion_rate(habit, days: int = 30) -> float:
    """
    Calculate the completion rate for a habit over the last N days.
    
    Args:
        habit: A Habit object
        days: Number of days to calculate rate for (default: 30)
    
    Returns:
        Completion rate as a percentage (0-100)
    """
    from django.utils import timezone
    
    start_date = timezone.now() - timedelta(days=days)
    completions_count = habit.completions.filter(completed_at__gte=start_date).count()
    
    # Calculate expected completions based on periodicity
    if habit.periodicity == 'daily':
        expected_completions = days
    else:  # weekly
        expected_completions = days // 7
    
    if expected_completions == 0:
        return 0.0
    
    rate = (completions_count / expected_completions) * 100
    return min(round(rate, 2), 100.0)  # Cap at 100%


def get_best_performing_habits(habits_queryset: QuerySet, limit: int = 5) -> List[Dict]:
    """
    Get the top performing habits based on current streak.
    
    Args:
        habits_queryset: QuerySet of Habit objects
        limit: Maximum number of habits to return
    
    Returns:
        List of top performing habits sorted by current streak
    """
    active_habits = filter(lambda h: h.is_active, habits_queryset)
    
    habits_with_streaks = list(map(
        lambda habit: {
            'id': habit.id,
            'task': habit.task,
            'periodicity': habit.periodicity,
            'current_streak': habit.get_current_streak(),
            'longest_streak': habit.get_longest_streak(),
        },
        active_habits
    ))
    
    # Sort by current streak (descending)
    sorted_habits = sorted(habits_with_streaks, key=lambda h: h['current_streak'], reverse=True)
    
    return sorted_habits[:limit]
