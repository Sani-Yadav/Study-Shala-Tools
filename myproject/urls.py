from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('notes/', include('notes.urls')),
    path('scanner/', include('scanner.urls')),
    path('resume/', include('resume.urls')),
    path('idcard/', include('idcard.urls')),
    path('employeeid/', include('employeeid.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
