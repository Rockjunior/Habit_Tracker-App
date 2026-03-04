from django.contrib import admin
from .models import Habit, HabitCompletion


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Admin panel for managing habits.
    
    See all habits at a glance, filter them, search for specific ones,
    and manage them directly from the admin dashboard.
    """
    list_display = ('task', 'periodicity', 'created_at', 'is_active', 'current_streak_display')
    list_filter = ('periodicity', 'is_active', 'created_at')
    search_fields = ('task',)
    ordering = ('-created_at',)
    
    def current_streak_display(self, obj):
        """Show the current streak right in the admin table.
        
        Makes it easy to see at a glance how well each habit is doing!
        """
        return obj.get_current_streak()
    current_streak_display.short_description = 'Current Streak'


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    """Admin panel for viewing all completions.
    
    See every single time someone completed a habit - useful for tracking
    activity and managing the completion history.
    """
    list_display = ('habit', 'completed_at')
    list_filter = ('habit', 'completed_at')
    ordering = ('-completed_at',)
    date_hierarchy = 'completed_at'
