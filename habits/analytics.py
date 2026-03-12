"""
Analytics module for Habit Tracker Application.

This module uses functional programming techniques (map, filter, reduce)
to transform habit data into dashboard insights.
"""

from typing import List, Dict
from functools import reduce
from datetime import datetime, timedelta
from django.db.models import QuerySet


def get_all_habits(habits_queryset: QuerySet) -> List[Dict]:
    """Return all active habits as dictionaries."""
    return list(
        map(
            lambda habit: {
                "id": habit.id,
                "task": habit.task,
                "periodicity": habit.periodicity,
                "created_at": habit.created_at,
                "is_active": habit.is_active,
                "current_streak": habit.get_current_streak(),
            },
            filter(lambda h: h.is_active, habits_queryset),
        )
    )


def get_habits_by_periodicity(habits_queryset: QuerySet, periodicity: str) -> List[Dict]:
    """Return active habits filtered by periodicity ('daily' or 'weekly')."""
    filtered_habits = filter(
        lambda h: h.is_active and h.periodicity == periodicity,
        habits_queryset,
    )

    return list(
        map(
            lambda habit: {
                "id": habit.id,
                "task": habit.task,
                "periodicity": habit.periodicity,
                "created_at": habit.created_at,
                "current_streak": habit.get_current_streak(),
            },
            filtered_habits,
        )
    )


def get_longest_streak_all_habits(habits_queryset: QuerySet) -> Dict:
    """Return the habit with the longest streak across all habits."""
    if not habits_queryset.exists():
        return {"habit": None, "streak": 0}

    habit_streaks = list(
        map(
            lambda habit: {"habit": habit, "streak": habit.get_longest_streak()},
            habits_queryset,
        )
    )

    max_streak_info = reduce(
        lambda max_item, current_item: current_item
        if current_item["streak"] > max_item["streak"]
        else max_item,
        habit_streaks,
        habit_streaks[0],
    )

    return {
        "habit": {
            "id": max_streak_info["habit"].id,
            "task": max_streak_info["habit"].task,
            "periodicity": max_streak_info["habit"].periodicity,
        },
        "streak": max_streak_info["streak"],
    }


def get_longest_streak_for_habit(habit) -> int:
    """Return the longest streak for a specific habit."""
    return habit.get_longest_streak()


def get_current_streaks_all_habits(habits_queryset: QuerySet) -> List[Dict]:
    """Return current streaks for all active habits."""
    return list(
        map(
            lambda habit: {
                "id": habit.id,
                "task": habit.task,
                "periodicity": habit.periodicity,
                "current_streak": habit.get_current_streak(),
            },
            filter(lambda h: h.is_active, habits_queryset),
        )
    )


def get_completion_stats(habits_queryset: QuerySet) -> Dict:
    """Calculate aggregate completion statistics for active habits."""
    if not habits_queryset.exists():
        return {
            "total_habits": 0,
            "daily_habits": 0,
            "weekly_habits": 0,
            "total_completions": 0,
            "average_streak": 0,
        }

    active_habits = list(filter(lambda h: h.is_active, habits_queryset))

    daily_count = len(list(filter(lambda h: h.periodicity == "daily", active_habits)))
    weekly_count = len(list(filter(lambda h: h.periodicity == "weekly", active_habits)))

    total_completions = reduce(
        lambda total, habit: total + habit.completions.count(),
        active_habits,
        0,
    )

    current_streaks = list(map(lambda h: h.get_current_streak(), active_habits))
    average_streak = sum(current_streaks) / len(current_streaks) if current_streaks else 0

    return {
        "total_habits": len(active_habits),
        "daily_habits": daily_count,
        "weekly_habits": weekly_count,
        "total_completions": total_completions,
        "average_streak": round(average_streak, 2),
    }


def get_struggling_habits(habits_queryset: QuerySet) -> List[Dict]:
    """Return active habits with current streak <= 1."""
    struggling = filter(
        lambda habit: habit.get_current_streak() <= 1,
        filter(lambda h: h.is_active, habits_queryset),
    )

    return list(
        map(
            lambda habit: {
                "id": habit.id,
                "task": habit.task,
                "periodicity": habit.periodicity,
                "current_streak": habit.get_current_streak(),
            },
            struggling,
        )
    )


def get_habits_completed_in_period(
    habits_queryset: QuerySet, start_date: datetime, end_date: datetime
) -> List[Dict]:
    """Return habits completed at least once between start_date and end_date."""

    def count_completions_in_period(habit):
        count = habit.completions.filter(
            completed_at__gte=start_date,
            completed_at__lte=end_date,
        ).count()
        return {
            "id": habit.id,
            "task": habit.task,
            "periodicity": habit.periodicity,
            "completions_in_period": count,
        }

    habits_with_completions = map(count_completions_in_period, habits_queryset)
    return list(filter(lambda h: h["completions_in_period"] > 0, habits_with_completions))


def calculate_completion_rate(habit, days: int = 30) -> float:
    """Calculate completion rate percentage for a habit over the last N days."""
    from django.utils import timezone

    start_date = timezone.now() - timedelta(days=days)
    completions_count = habit.completions.filter(completed_at__gte=start_date).count()

    if habit.periodicity == "daily":
        expected_completions = days
    else:
        expected_completions = days // 7

    if expected_completions == 0:
        return 0.0

    rate = (completions_count / expected_completions) * 100
    return min(round(rate, 2), 100.0)


def get_best_performing_habits(habits_queryset: QuerySet, limit: int = 5) -> List[Dict]:
    """Return top-performing active habits sorted by current streak descending."""
    active_habits = filter(lambda h: h.is_active, habits_queryset)

    habits_with_streaks = list(
        map(
            lambda habit: {
                "id": habit.id,
                "task": habit.task,
                "periodicity": habit.periodicity,
                "current_streak": habit.get_current_streak(),
                "longest_streak": habit.get_longest_streak(),
            },
            active_habits,
        )
    )

    sorted_habits = sorted(
        habits_with_streaks,
        key=lambda h: h["current_streak"],
        reverse=True,
    )

    return sorted_habits[:limit]
