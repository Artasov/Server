from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    path('', views.Shop, name='shop'),
    path('buy/', views.Buy, name='buy'),
    path('pay/', views.Pay, name='pay'),
    path('product/xLGM', views.Product, name='xL Guild Manager'),
    path('product/xLUMRA', views.Product, name='xLUMRA'),
    path('product/xLCracker', views.Product, name='xLCracker'),
    path('product/xLCracker', views.Product, name='xLCracker'),
    url(r'^download/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='download'),

]


