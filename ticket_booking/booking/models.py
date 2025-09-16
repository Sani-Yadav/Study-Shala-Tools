from django.db import models
from django.conf import settings

# Bus ya train ki information
class BusTrain(models.Model):
    name = models.CharField(max_length=100)            # Bus/Train ka naam
    starting_city = models.CharField(max_length=50)    # Journey start hone ka city
    ending_city = models.CharField(max_length=50)      # Journey end hone ka city
    date = models.DateField()                           # Travel date
    time = models.TimeField()                           # Travel time
    total_seats = models.IntegerField()                # Total seats
    available_seats = models.IntegerField()            # Abhi available seats
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Ticket price

    def __str__(self):
        return f"{self.name}: {self.starting_city} → {self.ending_city}"


# Booking details
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Kaun book kar raha hai
    bus_train = models.ForeignKey(BusTrain, on_delete=models.CASCADE)  # Kis bus/train ka ticket
    seat_number = models.IntegerField()                        # Seat number
    booking_time = models.DateTimeField(auto_now_add=True)     # Kab book kiya
    payment_status = models.BooleanField(default=False)        # Payment ho gaya ya nahi

    def __str__(self):
        return f"{self.user.username} - {self.bus_train.name} (Seat {self.seat_number})"
