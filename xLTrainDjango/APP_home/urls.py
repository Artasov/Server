from django.conf import settings
from django.conf.urls import url
from django.urls import include, re_path
from django.urls import path
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('shop/', include('APP_shop.urls'), name='shop'),
    path('task/', include('APP_task.urls'), name='tasks'),
    path('profile/', views.Profile, name='profile'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('password_reset/', views.PasswordReset, name='password_reset'),
    path('set_nickname/', views.SetNickname, name='set_nickname'),
    path('set_guild/', views.SetGuild, name='set_guild'),
    path('donate/', views.Donate, name='donate'),
    path('about/', views.About, name='about'),
    path('terms_and_conditions/', views.Terms_and_conditions, name='terms_and_conditions'),
    path('privacy_policy/', views.Privacy_policy, name='privacy_policy'),
    path('password_reset_confirmation/', views.PasswordResetConfirmation, name='password_reset_confirmation'),
    path('regconfirm/', views.RegistrateConfirmation, name='registrate_confirmation'),
    path('resume/', views.Resume, name='resume'),
    path('ideas/', views.Ideas, name='ideas'),

    path('api/program_auth/', views.ProgramAuth, name='program_auth'),
    path('api/set_hwid/', views.SetHWID, name='set_hwid'),

    re_path(r'download/(?P<path>.*)$', views.Download, name='download'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
