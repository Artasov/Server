from django.urls import path
from . import views
import os

urlpatterns = [
    path('', views.Tasks),
    path('first/', views.TaskFirst, name='task_first'),
    path('second/', views.TaskSecond, name='task_second'),
]