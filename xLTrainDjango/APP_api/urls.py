from django.urls import path

from . import views

urlpatterns = [  # /api/v1/
    path('users/', views.UserAPIView.as_view(), name='api-users'),
    path('user/<str:name>/', views.UserAPIViewByName.as_view(), name='api-user'),
    path('task/', views.RekrutoTask, name='rekruto_task'),
    path('random_str/', views.RandomStrAPIView, name='api-random_str')
]
