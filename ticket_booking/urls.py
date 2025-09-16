from django.urls import path, include

app_name = 'ticket_booking'

urlpatterns = [
    path('', include('ticket_booking.booking.urls')),
]
