
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sending.urls', namespace='sending')),
    path('message/', include('message.urls', namespace='message')),
]
