from django.shortcuts import render, redirect, get_object_or_404
from login.models import User
from booking.models import Contact
from booking.models import Rental, Booking
from django.contrib import messages
from django.http import HttpResponse
import datetime


def index(request):
    return render(request, 'booking/index.html', {})


def contact(request):
    if request.method == "GET":
        return render(request, "contact/contact.html", {})
    else:
        username = request.POST['name']
        gender = request.POST['gender']
        profile_pic = request.POST['profile_pic']
        phone_number = request.POST['phone']
        address = request.POST['address']
        data = Contact(name=username, gender=gender, profile_pic=profile_pic, phone_number=phone_number,
                       address=address)
        data.save()
        return render(request, "contact/contact.html", {'message': 'Thank you for contacting us.'})


def book(request):
    if request.method == "POST":
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        start_date = datetime.datetime.strptime(start_date, "%d/%b/%Y").date()
        end_date = datetime.datetime.strptime(end_date, "%d/%b/%Y").date()
        no_of_days = (end_date - start_date).days
        # data = Rental.objects.filter(is_available=True, no_of_days_advance__gte=no_of_days, start_date__lte=start_date)
        print(start_date)
        print(end_date)
        print(Booking.objects.all().values_list('start_day', 'end_day'))
        bookings_starting_within = Booking.objects.filter(start_day__lt=start_date, end_day__gt=start_date)
        bookings_ending_within = Booking.objects.filter(start_day__lt=end_date, end_day__gt=end_date)
        bookings_within = bookings_starting_within | bookings_ending_within
        not_available_rental_ids = bookings_within.values_list('rental__id')
        available_rentals = Rental.objects.exclude(id__in=not_available_rental_ids)
        request.session['no_of_days'] = no_of_days

        return render(request, 'booking/book.html', {'available_rentals': available_rentals})


    else:
        return redirect('booking:index')


def book_now(request, id):
    if request.session.get("username", None) and request.session.get("type", None) == 'customer':
        if request.session.get("no_of_days", 1):
            no_of_days = request.session['no_of_days']
            start_date = request.session['start_date']
            end_date = request.session['end_date']
            request.session['rental'] = id
            data = Rental.objects.get(id=id)
            bill = data.price * int(no_of_days)
            request.session['bill'] = float(bill)
            user = data.owner.username
            return render(request, "booking/book-now.html",
                          {"no_of_days": no_of_days, "rental_no": id, "data": data, "bill": bill,
                           "User": user, "start": start_date, "end": end_date})
        else:
            return redirect("booking:index")
    else:
        next = "book-now/" + id
        return redirect('login:user-login')


def book_confirm(request):
    booked_on = request.session['booked_on']
    start_date = request.session['start_date']
    end_date = request.session['end_date']
    username = request.session['username']
    user = User.objects.get(id=username)
    rental = Rental.objects.get(id=booked_on)
    amount = request.session['bill']
    start_date = datetime.datetime.strptime(start_date, "%d/%b/%Y").date()
    end_date = datetime.datetime.strptime(end_date, "%d/%b/%Y").date()
    data = Booking(rental=rental, start_day=start_date, end_day=end_date, amount=amount, user=user)
    data.save()
    rental.is_available = False
    rental.save()
    del request.session['start_date']
    del request.session['end_date']
    del request.session['bill']
    del request.session['rental']
    messages.info(request, "Yacht has been successfully booked")
    return redirect('booking:user-dashboard')


def cancel_yacht(request, id):
    data = get_object_or_404(Booking, id=id)
    rental = data.rental
    rental.is_available = True
    rental.save()
    data.delete()
    return HttpResponse("Booking Cancelled Successfully")


def delete_yacht(request, id):
    data = get_object_or_404(Rental, id=id)
    owner = data.owner.username
    if owner == request.session['username']:
        data.delete()
        return HttpResponse("You have deleted the rental successfully")
    else:
        return HttpResponse("Invalid Request")

