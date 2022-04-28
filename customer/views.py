from django.shortcuts import render, redirect
from login.models import User
from booking.models import Booking
import datetime


def dashboard(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'manager':
        return redirect('manager_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        username = request.session['username']
        data = User.objects.get(username=username)
        booking_data = Booking.objects.filter(user=data).order_by('-id')
        counts = booking_data.filter(end_day__lt=datetime.datetime.now()).count()
        available = len(booking_data) - counts
        return render(request, "user_dash/index.html", {"data": booking_data, "count": counts, "available": available})
    else:
        return redirect("customer:user-dashboard")


def details(request, user, booking_on):
    if not request.session.get('username', None):
        return redirect('manager_login')
    if request.session.get('username', None) and request.session.get('type', None) == 'customer':
        return redirect('customer:user-dashboard')
    try:
        booking_data = Booking.objects.get(id=booking_on)
        user = User.objects.get(id=user)
        return render(request,
                      "user_dash/details.html",
                      {"user": user,
                       "booking_data":
                           booking_data
                       }
                      )
    except:
        return redirect("customer:user-details")
