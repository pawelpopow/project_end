from django.shortcuts import render, redirect
from login.models import User
from booking.models import Rental
from django.contrib import messages


def dashboard(request):
    if not request.session.get('username', None):
        return redirect('rentel:manager-dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'user':
        return redirect('customer:user-dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'manager':
        username = request.session['username']
        data = User.objects.get(id=username)
        data1 = data.rental_set.all()
        booked = data1.filter(is_available=False).count()
        print(booked)
        return render(request, "manager_dash/index.html",
                      {"data1": data1, "manager": data, "booked": booked})
    else:
        return redirect("login:user-login")
        # return redirect('rentel:manager-dashboard')


def add_rental(request):
    if not request.session.get('username', None):
        return redirect('login:user-login')
    if request.session.get('username', None) and request.session.get('type', None) == 'user':
        return redirect('customer:user-dashboard')
    if request.method == "GET":
        return render(request, "manager_dash/add-rental.html", {})
    else:
        name_yacht = request.POST['name_yacht']
        price = request.POST['price']
        rental_image = request.FILES.get('rental_image', None)
        error = []
        if (len(name_yacht) < 1):
            error.append(1)
            messages.warning(request, "Enter the name of the yacht")
        if (len(price) <= 2):
            error.append(1)
            messages.warning(request, "Please enter price")
        if (not len(error)):
            manager = request.session['username']
            manager = User.objects.get(username=manager)
            rental = Rental(name_yacht=name_yacht, price=price, rental_image=rental_image,
                            manager=manager)
            rental.save()
            messages.info(request, "Rental Added Successfully")
            return redirect('rental:dashboard1')
        else:
            return redirect('rentel:add-rental')


def update_rental(request, name_yacht):
    if not request.session.get('username', None):
        return redirect('login:manager_login')
    if request.session.get('username', None) and request.session.get('type', None) == 'User':
        return redirect('user_dashboard')
    rental = Rental.objects.get(id=name_yacht)
    if request.method == "GET":
        return render(request, "manager_dash/edit-rental.html", {"name_yacht": name_yacht})
    else:
        price = request.POST['price']
        no_of_days_advance = request.POST['no_of_days_advance']
        error = []
        if (len(price) <= 2):
            error.append(1)
            messages.warning(request, "Please enter correct price")
        if (len(no_of_days_advance) < 1):
            error.append(1)
            messages.warning(request, "Please add valid no of days a user can book rental in advance.")
        if (not len(error)):
            manager = request.session['username']
            manager = User.objects.get(username=manager)
            User.price = price
            User.no_of_days_advance = no_of_days_advance
            User.save()
            messages.info(request, "Rental Data Updated Successfully")
            return redirect('rentel:dashboard')
        else:
            return redirect('rentel:update-rental' + rental.name_yacht, {"rental": rental})
