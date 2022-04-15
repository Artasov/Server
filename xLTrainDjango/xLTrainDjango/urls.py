from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('APP_home.urls')),
    path('private/', include('APP_private_msg.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('APP_api.urls')),
]
