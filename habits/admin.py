from django.contrib import admin
from .models import Habit, HabitCompletion


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Admin interface for Habit model."""
    list_display = ('task', 'periodicity', 'created_at', 'is_active', 'current_streak_display')
    list_filter = ('periodicity', 'is_active', 'created_at')
    search_fields = ('task',)
    ordering = ('-created_at',)
    
    def current_streak_display(self, obj):
        """Display the current streak for the habit."""
        return obj.get_current_streak()
    current_streak_display.short_description = 'Current Streak'


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    """Admin interface for HabitCompletion model."""
    list_display = ('habit', 'completed_at')
    list_filter = ('habit', 'completed_at')
    ordering = ('-completed_at',)
    date_hierarchy = 'completed_at'
