from django.urls import path

from . import views

urlpatterns = [  # /api/v1/
    path('users/', views.UserAPIView.as_view(), name='api-users'),
    path('user/<str:name>/', views.UserAPIViewByName.as_view(), name='api-user'),
    path('random_str/', views.RandomStrAPIView, name='api-random_str'),
    path('program_auth/', views.ProgramAuth, name='program_auth'),
    path('set_hwid/', views.SetHWID, name='set_hwid'),
    path('product_version/<str:product>/', views.ProductVersion, name='product_version'),
]
