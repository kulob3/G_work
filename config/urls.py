from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sending.urls', namespace='sending')),
    path('message/', include('message.urls', namespace='message')),
    path('clients/', include('clients.urls', namespace='client')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('users/', include('users.urls', namespace='users')),
    path('doctors/', include('doctors.urls', namespace='doctors')),
    path('service/', include('service.urls', namespace='service')),
    path('appointment/', include('appointment.urls', namespace='appointment')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
