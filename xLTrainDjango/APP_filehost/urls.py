from django.conf import settings
from django.conf.urls import url
from django.urls import include, re_path
from django.urls import path
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.UploadFile, name='upload_file'),
    path('<int:pk>/', views.ReadUpload, name='read_upload'),
    path('<int:pk>/del/', views.DeleteUpload, name='del_upload'),
]
