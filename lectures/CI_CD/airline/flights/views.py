from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    flights = Flight.objects.all() 
    return render(request, "flights/index.html", {
        "flights": flights 
    })

def flight(request, flight_id):
    flight = Flight.objects.get(pk = flight_id)
    passengers = flight.passengers.all()
    return render(request, 'flights/flight.html', {
        "flight": flight,
        'passengers': passengers,
        'non_passengers': Passenger.objects.exclude(flights = flight).all()
    }) 

def book(request, flight_id):
    if request.method == 'POST':
        flight = Flight.objects.get(pk = flight_id)
        passenger = Passenger.objects.get(pk = int(request.POST['passenger']))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('flight', args=(flight.id, )))