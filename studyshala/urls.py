from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import home, signup

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', signup, name='signup'),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # App URLs
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('notes/', include('notes.urls', namespace='notes')),
    path('scanner/', include('scanner.urls', namespace='scanner')),
    path('idcard/', include('idcard.urls', namespace='idcard')),
    path('resume/', include('resume.urls', namespace='resume')),
    path('employeeid/', include('employeeid.urls', namespace='employeeid')),
    path('attendance/', include('qr_attendance.attendance.urls', namespace='attendance')),
    path('health/', include('health_assist.urls', namespace='health_assist')),
    path('media-downloader/', include('media_downloader.downloader.urls', namespace='media_downloader')),
    path('satellite-tracker/', include('satellite_tracker.tracker.urls', namespace='satellite_tracker')),
    path('farm/', include('farm.urls', namespace='farm')),
    path('ticket-booking/', include(('ticket_booking.urls', 'ticket_booking'), namespace='ticket_booking')),
    path('social-post/', include('social_post.urls')),
    path('sarkarisahyogi/', include('sarkarisahyogi.jobform.urls', namespace='sarkarisahyogi')),
    path('feedback/', include('qr_feedback.qr_feedback.urls')),
    path('political-id/', include('political_id.id_card_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)