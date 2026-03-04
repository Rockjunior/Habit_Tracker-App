"""
Management command to populate the database with sample data.

Run this to fill your app with 5 realistic example habits and 4 weeks of tracking data.
Great for testing, demos, or just playing around with the app!
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from habits.models import Habit, HabitCompletion
import random


class Command(BaseCommand):
    help = 'Fill your database with 5 example habits and 4 weeks of realistic tracking data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate database with predefined habits...'))
        
        # Clear existing data
        HabitCompletion.objects.all().delete()
        Habit.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing habit data'))
        
        # Define 5 predefined habits
        habits_data = [
            {
                'task': 'Drink 8 glasses of water',
                'periodicity': 'daily',
                'completion_rate': 0.85,  # 85% completion rate
            },
            {
                'task': 'Exercise for 30 minutes',
                'periodicity': 'daily',
                'completion_rate': 0.70,  # 70% completion rate
            },
            {
                'task': 'Read a book for 20 minutes',
                'periodicity': 'daily',
                'completion_rate': 0.60,  # 60% completion rate
            },
            {
                'task': 'Attend yoga class',
                'periodicity': 'weekly',
                'completion_rate': 0.75,  # 75% completion rate
            },
            {
                'task': 'Grocery shopping',
                'periodicity': 'weekly',
                'completion_rate': 0.90,  # 90% completion rate
            },
        ]
        
        # Set creation date to 4 weeks ago
        creation_date = timezone.now() - timedelta(weeks=4)
        
        for habit_data in habits_data:
            # Create the habit
            habit = Habit.objects.create(
                task=habit_data['task'],
                periodicity=habit_data['periodicity'],
                created_at=creation_date,
                is_active=True
            )
            
            self.stdout.write(f'Created habit: {habit.task} ({habit.periodicity})')
            
            # Generate 4 weeks of test data
            self._generate_completions(habit, habit_data['completion_rate'])
            
            # Display streak information
            current_streak = habit.get_current_streak()
            longest_streak = habit.get_longest_streak()
            self.stdout.write(
                f'  Current streak: {current_streak}, '
                f'Longest streak: {longest_streak}'
            )
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {len(habits_data)} habits with 4 weeks of data!'))
    
    def _generate_completions(self, habit, completion_rate):
        """
        Create realistic completion data for a habit over the past 4 weeks.
        
        Based on a completion rate (like 85%), randomly decides whether the habit
        was completed on each day/week to create realistic-looking data.
        
        Args:
            habit: The habit to generate data for
            completion_rate: What % of days/weeks should have completions (0.0 to 1.0)
        """
        now = timezone.now()
        
        if habit.periodicity == 'daily':
            # Generate for 28 days (4 weeks)
            for day_offset in range(28):
                completion_date = now - timedelta(days=(27 - day_offset))
                
                # Randomly decide if habit was completed based on completion rate
                if random.random() < completion_rate:
                    # Add some time variation within the day
                    hour = random.randint(6, 22)
                    minute = random.randint(0, 59)
                    completion_datetime = completion_date.replace(
                        hour=hour, 
                        minute=minute,
                        second=0,
                        microsecond=0
                    )
                    
                    HabitCompletion.objects.create(
                        habit=habit,
                        completed_at=completion_datetime
                    )
        
        else:  # weekly
            # Generate for 4 weeks
            for week_offset in range(4):
                completion_date = now - timedelta(weeks=(3 - week_offset))
                
                # Randomly decide if habit was completed based on completion rate
                if random.random() < completion_rate:
                    # Complete on a random day of the week
                    day_offset = random.randint(0, 6)
                    hour = random.randint(6, 22)
                    minute = random.randint(0, 59)
                    
                    completion_datetime = completion_date - timedelta(days=completion_date.weekday()) + timedelta(days=day_offset)
                    completion_datetime = completion_datetime.replace(
                        hour=hour,
                        minute=minute,
                        second=0,
                        microsecond=0
                    )
                    
                    HabitCompletion.objects.create(
                        habit=habit,
                        completed_at=completion_datetime
                    )
        
        completion_count = habit.completions.count()
        self.stdout.write(f'  Generated {completion_count} completions')
