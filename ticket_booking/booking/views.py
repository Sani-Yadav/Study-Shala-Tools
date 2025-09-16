from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import BusTrain, Booking
import json

def home(request):
    return render(request, 'booking/home.html')

def search(request):
    if request.method == "GET":
        starting_city = request.GET.get("starting_city")
        ending_city = request.GET.get("ending_city")
        date = request.GET.get("date")

        # Filter using updated field names
        results = BusTrain.objects.filter(
            starting_city=starting_city, 
            ending_city=ending_city, 
            date=date
        )
        return render(request, "search.html", {"results": results})
    return render(request, "search.html")


@login_required
def book_ticket(request, id):
    bus_train = BusTrain.objects.get(id=id)
    
    if bus_train.available_seats > 0:
        # Seat number calculate
        seat_number = bus_train.total_seats - bus_train.available_seats + 1
        
        # Booking create
        booking = Booking.objects.create(
            user=request.user,
            bus_train=bus_train,
            seat_number=seat_number,
            payment_status=True  # Demo ke liye True
        )
        
        # Available seats update
        bus_train.available_seats -= 1
        bus_train.save()
        
        return render(request, "confirmation.html", {"booking": booking})
    
    # Agar seats nahi hai
    return render(request, "error.html", {"message": "No seats available"})



    # new views 
   

@csrf_exempt
def confirm_seats(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        seats = data.get("seats", [])
        bus_train = BusTrain.objects.get(id=id)

        booked_seats = Booking.objects.filter(bus_train=bus_train).values_list('seat_number', flat=True)
        for seat in seats:
            if int(seat) in booked_seats:
                return JsonResponse({"status": "error", "message": f"Seat {seat} already booked!"})
        
        # Book seats
        for seat in seats:
            Booking.objects.create(
                user=request.user,
                bus_train=bus_train,
                seat_number=int(seat),
                payment_status=True  # demo
            )
            bus_train.available_seats -= 1
        bus_train.save()

        return JsonResponse({"status": "success"})

