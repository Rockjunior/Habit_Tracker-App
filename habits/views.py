"""
Views for the Habit Tracker application.

This module contains all the views for handling user interactions with habits.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from .models import Habit, HabitCompletion
from . import analytics


def home(request):
    """
    Home page view showing overview of all habits.
    
    Displays a summary of habits with their current streaks and quick actions.
    """
    habits = Habit.objects.filter(is_active=True)
    
    # Get statistics using analytics module
    stats = analytics.get_completion_stats(Habit.objects.all())
    best_performers = analytics.get_best_performing_habits(Habit.objects.all(), limit=3)
    struggling = analytics.get_struggling_habits(Habit.objects.all())
    
    context = {
        'habits': habits,
        'stats': stats,
        'best_performers': best_performers,
        'struggling_habits': struggling,
    }
    
    return render(request, 'habits/home.html', context)


def habit_list(request):
    """
    Display a list of all active habits.
    """
    periodicity_filter = request.GET.get('periodicity', '')
    
    if periodicity_filter:
        habits = Habit.objects.filter(is_active=True, periodicity=periodicity_filter)
    else:
        habits = Habit.objects.filter(is_active=True)
    
    context = {
        'habits': habits,
        'periodicity_filter': periodicity_filter,
    }
    
    return render(request, 'habits/habit_list.html', context)


def habit_detail(request, habit_id):
    """
    Display detailed information about a specific habit.
    
    Shows completion history, streaks, and analytics for the habit.
    """
    habit = get_object_or_404(Habit, id=habit_id)
    
    # Get recent completions (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_completions = habit.completions.filter(completed_at__gte=thirty_days_ago).order_by('-completed_at')
    
    # Calculate completion rate
    completion_rate = analytics.calculate_completion_rate(habit, days=30)
    
    # Get longest streak
    longest_streak = habit.get_longest_streak()
    current_streak = habit.get_current_streak()
    
    context = {
        'habit': habit,
        'recent_completions': recent_completions,
        'completion_rate': completion_rate,
        'longest_streak': longest_streak,
        'current_streak': current_streak,
        'is_completed_today': habit.is_completed_today(),
    }
    
    return render(request, 'habits/habit_detail.html', context)


def add_habit(request):
    """
    Handle the creation of a new habit.
    """
    if request.method == 'POST':
        task = request.POST.get('task', '').strip()
        periodicity = request.POST.get('periodicity', 'daily')
        
        if not task:
            messages.error(request, 'Habit task cannot be empty.')
            return redirect('add_habit')
        
        if periodicity not in ['daily', 'weekly']:
            messages.error(request, 'Invalid periodicity. Choose daily or weekly.')
            return redirect('add_habit')
        
        habit = Habit.objects.create(
            task=task,
            periodicity=periodicity,
            is_active=True
        )
        
        messages.success(request, f'Habit "{habit.task}" created successfully!')
        return redirect('habit_detail', habit_id=habit.id)
    
    return render(request, 'habits/add_habit.html')


def complete_habit(request, habit_id):
    """
    Mark a habit as completed for the current period.
    """
    habit = get_object_or_404(Habit, id=habit_id)
    
    # Check if already completed today
    if habit.is_completed_today():
        messages.warning(request, f'You have already completed "{habit.task}" for this period.')
    else:
        habit.complete_task()
        messages.success(request, f'Great job! You completed "{habit.task}"!')
    
    # Redirect to the referring page or home
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def delete_habit(request, habit_id):
    """
    Delete (deactivate) a habit.
    """
    habit = get_object_or_404(Habit, id=habit_id)
    
    if request.method == 'POST':
        habit.is_active = False
        habit.save()
        messages.success(request, f'Habit "{habit.task}" has been deleted.')
        return redirect('home')
    
    context = {'habit': habit}
    return render(request, 'habits/delete_habit.html', context)


def analytics_view(request):
    """
    Display analytics dashboard with comprehensive statistics.
    
    Shows all analytics from the functional programming analytics module.
    """
    habits = Habit.objects.all()
    
    # Get all analytics using functional programming module
    all_habits = analytics.get_all_habits(habits)
    daily_habits = analytics.get_habits_by_periodicity(habits, 'daily')
    weekly_habits = analytics.get_habits_by_periodicity(habits, 'weekly')
    longest_streak_info = analytics.get_longest_streak_all_habits(habits)
    current_streaks = analytics.get_current_streaks_all_habits(habits)
    stats = analytics.get_completion_stats(habits)
    best_performers = analytics.get_best_performing_habits(habits, limit=5)
    struggling = analytics.get_struggling_habits(habits)
    
    context = {
        'all_habits': all_habits,
        'daily_habits': daily_habits,
        'weekly_habits': weekly_habits,
        'longest_streak_info': longest_streak_info,
        'current_streaks': current_streaks,
        'stats': stats,
        'best_performers': best_performers,
        'struggling_habits': struggling,
    }
    
    return render(request, 'habits/analytics.html', context)


def api_habit_list(request):
    """
    API endpoint to get all habits in JSON format.
    """
    habits = Habit.objects.filter(is_active=True)
    habits_data = analytics.get_all_habits(habits)
    
    return JsonResponse({
        'success': True,
        'habits': habits_data,
        'count': len(habits_data)
    })


def api_analytics(request):
    """
    API endpoint to get analytics data in JSON format.
    """
    habits = Habit.objects.all()
    
    stats = analytics.get_completion_stats(habits)
    longest_streak = analytics.get_longest_streak_all_habits(habits)
    best_performers = analytics.get_best_performing_habits(habits, limit=5)
    
    return JsonResponse({
        'success': True,
        'statistics': stats,
        'longest_streak': longest_streak,
        'best_performers': best_performers,
    })
