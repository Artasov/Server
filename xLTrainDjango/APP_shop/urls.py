from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    path('', views.Shop, name='shop'),
    path('buy/', views.Buy, name='buy'),
    path('pay/', views.Pay, name='pay'),
    path('product/<str:product>', views.Product, name='product'),
]


