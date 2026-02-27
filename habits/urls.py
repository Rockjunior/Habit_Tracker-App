"""
URL configuration for the habits app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('habits/', views.habit_list, name='habit_list'),
    path('habits/add/', views.add_habit, name='add_habit'),
    path('habits/<int:habit_id>/', views.habit_detail, name='habit_detail'),
    path('habits/<int:habit_id>/complete/', views.complete_habit, name='complete_habit'),
    path('habits/<int:habit_id>/delete/', views.delete_habit, name='delete_habit'),
    path('analytics/', views.analytics_view, name='analytics'),
    
    # API endpoints
    path('api/habits/', views.api_habit_list, name='api_habit_list'),
    path('api/analytics/', views.api_analytics, name='api_analytics'),
]
