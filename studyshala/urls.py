from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('notes/', include('notes.urls', namespace='notes')),
    path('scanner/', include('scanner.urls', namespace='scanner')),
    path('idcard/', include('idcard.urls', namespace='idcard')),
    path('resume/', include('resume.urls', namespace='resume')),
    path('employeeid/', include('employeeid.urls', namespace='employeeid')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)