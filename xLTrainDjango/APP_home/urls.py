from django.conf import settings
from django.conf.urls import url
from django.urls import include, re_path
from django.urls import path
from django.views.static import serve

from . import views


urlpatterns = [
    path('shop/', include('APP_shop.urls'), name='shop'),
    path('private/', include('APP_private_msg.urls')),
    path('host/', include('APP_filehost.urls')),
    path('', views.Home, name='home'),
    path('registration/', views.Registration, name='registration'),
    path('regconfirm/<str:CODE>/', views.RegistrateConfirmation, name='registrate_confirmation'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('password_reset/', views.PasswordReset, name='password_reset'),
    path('password_reset_confirmation/<str:CODE>/', views.PasswordResetConfirmation, name='password_reset_confirmation'),
    path('profile/', views.Profile, name='profile'),
    path('donate/', views.Donate, name='donate'),
    path('about/', views.About, name='about'),
    path('terms_and_conditions/', views.Terms_and_conditions, name='terms_and_conditions'),
    path('privacy_policy/', views.Privacy_policy, name='privacy_policy'),
    path('resume/', views.Resume, name='resume'),
    path('ideas/', views.Ideas, name='ideas'),
    path('more/', views.MoreView, name='more'),

    re_path(r'download/(?P<path>.*)$', views.Download, name='download'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
