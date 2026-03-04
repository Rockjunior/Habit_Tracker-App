from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from typing import List, Optional


class Habit(models.Model):
    """
    A habit you want to build and track.
    
    A habit is simply something you want to do regularly - brush your teeth daily,
    go to yoga weekly, whatever! The app tracks when you complete it and keeps
    count of your awesome streaks.
    
    Attributes:
        task (str): What you're trying to accomplish
        periodicity (str): How often ('daily' or 'weekly')
        created_at (datetime): When you started tracking this habit
        is_active (bool): Whether you're currently working on it
    """
    
    PERIODICITY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    
    task = models.CharField(
        max_length=255,
        help_text="Description of the habit task"
    )
    
    periodicity = models.CharField(
        max_length=10,
        choices=PERIODICITY_CHOICES,
        default='daily',
        help_text="How often the habit should be completed"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the habit was created"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the habit is currently being tracked"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'
    
    def __str__(self):
        return f"{self.task} ({self.periodicity})"
    
    def complete_task(self, completion_date: Optional[datetime] = None) -> 'HabitCompletion':
        """Record a completion for this habit.
        
        Mark it done today, or log a past completion if you forgot to check it off.
        Creates a timestamp record so we know exactly when you crushed this habit!
        
        Args:
            completion_date: When you completed it (defaults to right now)
        
        Returns:
            The completion record we just created
        """
        if completion_date is None:
            completion_date = timezone.now()
        
        completion = HabitCompletion.objects.create(
            habit=self,
            completed_at=completion_date
        )
        return completion
    
    def get_completions(self) -> models.QuerySet:
        """
        Get all completions for this habit.
        
        Returns:
            QuerySet: All completion records for this habit
        """
        return self.completions.all().order_by('completed_at')
    
    def get_current_streak(self) -> int:
        """How many days/weeks have you kept this going without breaking?
        
        This is the "magic number" - your current unbroken streak. Build it up!
        """
        """
        Calculate the current streak for this habit.
        
        A streak is the number of consecutive periods where the habit was completed
        at least once. The streak breaks if a period is missed.
        
        Returns:
            int: Current streak count in periods
        """
        completions = self.get_completions()
        if not completions.exists():
            return 0
        
        # Get the period duration
        period_delta = timedelta(days=1) if self.periodicity == 'daily' else timedelta(weeks=1)
        
        # Start from today and work backwards
        current_period_start = self._get_period_start(timezone.now())
        streak = 0
        
        # Check if there's a completion in the current period
        has_current = completions.filter(
            completed_at__gte=current_period_start,
            completed_at__lt=current_period_start + period_delta
        ).exists()
        
        if not has_current:
            # If no completion in current period, check the most recent period
            current_period_start -= period_delta
            has_current = completions.filter(
                completed_at__gte=current_period_start,
                completed_at__lt=current_period_start + period_delta
            ).exists()
            
            if not has_current:
                return 0
        
        # Count consecutive periods with completions
        check_period_start = current_period_start
        while True:
            has_completion = completions.filter(
                completed_at__gte=check_period_start,
                completed_at__lt=check_period_start + period_delta
            ).exists()
            
            if has_completion:
                streak += 1
                check_period_start -= period_delta
            else:
                break
            
            # Safety check: don't go before habit creation
            if check_period_start < self.created_at:
                break
        
        return streak
    
    def get_longest_streak(self) -> int:
        """Your personal best streak for this habit.
        
        This is your record - the longest unbroken streak you've ever achieved.
        Something to be proud of!
        """
        """
        Calculate the longest streak ever achieved for this habit.
        
        Returns:
            int: Longest streak count in periods
        """
        completions = self.get_completions()
        if not completions.exists():
            return 0
        
        period_delta = timedelta(days=1) if self.periodicity == 'daily' else timedelta(weeks=1)
        
        # Get all unique periods with completions
        periods_with_completions = set()
        for completion in completions:
            period_start = self._get_period_start(completion.completed_at)
            periods_with_completions.add(period_start)
        
        if not periods_with_completions:
            return 0
        
        # Sort periods
        sorted_periods = sorted(periods_with_completions)
        
        # Find longest consecutive sequence
        longest_streak = 1
        current_streak = 1
        
        for i in range(1, len(sorted_periods)):
            expected_next = sorted_periods[i-1] + period_delta
            if sorted_periods[i] == expected_next:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        
        return longest_streak
    
    def _get_period_start(self, dt: datetime) -> datetime:
        """
        Get the start of the period that contains the given datetime.
        
        Args:
            dt: The datetime to find the period start for
        
        Returns:
            datetime: Start of the period
        """
        if self.periodicity == 'daily':
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        else:  # weekly
            # Get Monday of the week
            days_since_monday = dt.weekday()
            monday = dt - timedelta(days=days_since_monday)
            return monday.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def is_completed_today(self) -> bool:
        """Did you already complete this habit today (or this week)?
        
        Checks if you've already got a completion recorded for the current period.
        """
        """
        Check if the habit has been completed in the current period.
        
        Returns:
            bool: True if completed in the current period, False otherwise
        """
        period_start = self._get_period_start(timezone.now())
        period_delta = timedelta(days=1) if self.periodicity == 'daily' else timedelta(weeks=1)
        
        return self.completions.filter(
            completed_at__gte=period_start,
            completed_at__lt=period_start + period_delta
        ).exists()


class HabitCompletion(models.Model):
    """
    A single time you marked a habit as complete.
    
    Every time you click "Done!" on a habit, we create one of these records.
    It's basically a timestamp saying "yes, I did this thing!" These records
    add up to create your streaks and show your awesome history.
    
    Attributes:
        habit (Habit): Which habit you completed
        completed_at (datetime): The exact moment you completed it
    """
    
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='completions',
        help_text="The habit that was completed"
    )
    
    completed_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the habit was completed"
    )
    
    class Meta:
        ordering = ['-completed_at']
        verbose_name = 'Habit Completion'
        verbose_name_plural = 'Habit Completions'
    
    def __str__(self):
        return f"{self.habit.task} completed at {self.completed_at}"
