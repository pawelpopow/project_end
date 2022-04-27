from django.shortcuts import render, redirect
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
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        state = request.POST['state']
        data = Contact(name=username, gender=gender, profile_pic=profile_pic, phone_number=phone_number,
                       address=address, state=state)
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
        start_available_rental_ids = Booking.objects.filter(start_day__gt=start_date, start_day__lt=end_date)
        print(start_available_rental_ids)
        end_available_rental_ids = Booking.objects.filter(end_day__gt=start_date, end_day__lt=end_date)
        available_rental_ids = start_available_rental_ids | end_available_rental_ids
        print(end_available_rental_ids)
        b_ids = available_rental_ids.values_list("id")
        a = Booking.objects.exclude(id__in=b_ids)
        available_rental_ids = a.values_list("rental", flat=True)
        print(available_rental_ids)
        available_rentals = Rental.objects.filter(id__in=available_rental_ids)
        request.session['no_of_days'] = no_of_days
        return render(request, 'booking/book.html', {'available_rentals': available_rentals})


    else:
        return redirect('booking:index')


def book_now(request, name_yacht):
    if request.session.get("username", None) and request.session.get("type", None) == 'user':
        if request.session.get("no_of_days", 1):
            no_of_days = request.session['no_of_days']
            start_date = request.session['start_date']
            end_date = request.session['end_date']
            request.session['rental'] = id
            data = Rental.objects.get(id=name_yacht)
            bill = data.price * int(no_of_days)
            request.session['bill'] = bill
            user = data.manager.username
            return render(request, "booking/book-now.html",
                          {"no_of_days": no_of_days, "rental_no": id, "data": data, "bill": bill,
                           "User": user, "start": start_date, "end": end_date})
        else:
            return redirect("booking:index")
    else:
        next = "book-now/" + id
        return redirect('login:user-login')


def book_confirm(request):
    rental = request.session['rental']
    username = request.session['username']
    user = User.objects.get(username=username)
    rental = Rental.objects.get(id=rental)
    amount = request.session['bill']
    data = Booking(rental=rental, amount=amount, user=user)
    data.save()
    rental.is_available = False
    rental.save()
    del request.session['start_date']
    del request.session['end_date']
    del request.session['bill']
    del request.session['name_yacht']
    messages.info(request, "Yacht has been successfully booked")
    return redirect('booking:user-dashboard')


def cancel_yacht(request, booked_on):
    data = Booking.objects.get(id=booked_on)
    rental = data.rental
    rental.is_available = True
    rental.save()
    data.delete()
    return HttpResponse("Booking Cancelled Successfully")


def delete_yacht(request, name_yacht):
    data = Rental.objects.get(id=name_yacht)
    owner = data.owner.username
    if owner == request.session['username']:
        data.delete()
        return HttpResponse("You have deleted the rental successfully")
    else:
        return HttpResponse("Invalid Request")
