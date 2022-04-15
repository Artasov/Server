from django.urls import path

from . import views

urlpatterns = [
    path('msg/', views.PrivateMsg, name='private-msg'),
    path('msg/<str:key>/', views.PrivateMsg, name='private-msg-redirect-to-read'),
    path('msg/<str:key>/read/', views.PrivateMsgRead, name='private-msg-read'),
]
