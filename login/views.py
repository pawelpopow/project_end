from django.shortcuts import render, redirect
from login.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages


def user_login(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'user':
        print(10)
        return redirect('user-dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'manager':
        print(11)
        return redirect('manager-dashboard')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not len(username):
            messages.warning(request, "Username field is empty")
            print(1)
            redirect('user-login')
        elif not len(password):
            messages.warning(request, "Password field is empty")
            print(2)
            redirect('login:user-login')
        else:
            print(3)
            pass
        if User.objects.filter(username=username):
            user = User.objects.filter(username=username)[0]
            password_hash = user.password
            res = check_password(password, password_hash)
            if res == 1:
                request.session['username'] = username
                request.session['type'] = 'customer'
                print(4)
                return render(request, 'booking/index.html', {})
            else:
                messages.warning(request, "Username or password is incorrect")
                print(5)
                redirect('user-login')
        else:
            messages.warning(request, "No, Account exist for the given Username")
            print(6)
            redirect('login:user-login')
    # else:
    #     print(7)
    #     redirect('login:user-login')
    print(8)
    return render(
        request,
        'login/user_login.html',
        {}
    )


def manager_login(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'user':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'manager':
        return redirect('manager_dashboard')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not len(username):
            messages.warning(request, "Username field is empty")
            redirect('login:manager-login')
        elif not len(password):
            messages.warning(request, "Password field is empty")
            redirect('login:manager-login')
        else:
            pass
        if User.objects.filter(username=username):
            user = User.objects.filter(username=username)[0]
            password_hash = user.password
            res = check_password(password, password_hash)
            if res == 1:
                request.session['username'] = username
                request.session['type'] = 'manager'
                return render(request, 'booking/index.html', {})
            else:
                messages.warning(request, "Username or password is incorrect")
                redirect('login:manager_login')
        else:
            messages.warning(request, "No, Account exist for the given Username")
            redirect('login:manager_login')
    else:
        redirect('login:manager-login')
    return render(request, 'login/manager_login.html', {})


def user_signup(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'user':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'manager':
        return redirect('manager_dashboard')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(username=username) or User.objects.filter(email=email):
            messages.warning(request, "Account already exist, please Login to continue")
        else:
            password = request.POST['password']
            address = request.POST['address']
            profile_pic = request.FILES.get('profile_pic', None)
            phone_number = request.POST['phone_number']
            state = request.POST['state']
            error = []
            if (len(password) < 3):
                error.append(1)
                messages.warning(request, "Password Field must be greater than 3 character.")
            if (len(address) < 5):
                error.append(1)
                messages.warning(request, "Address Field must be greater than 5 character.")
            if (len(state) == 0):
                error.append(1)
                messages.warning(request, "State field can't be empty")
            if (len(phone_number) != 10):
                error.append(1)
                messages.warning(request, "Valid Phone number is a 10 digit-integer.")
            if (len(error) == 0):
                password_hash = make_password(password)
                user = User(username=username, password=password_hash, email=email, phone_number=phone_number,
                            address=address, state=state, profile_pic=profile_pic)

                user.save()
                messages.info(request, "Account Created Successfully, please Login to continue")
                redirect('login:user-signup')
            else:
                redirect('login:user-signup')

    else:
        redirect('login:user-signup')
    return render(request,
                  'login/user_login.html',
                  {}
                  )


def manager_signup(request):
    if request.session.get('username', None) and request.session.get('type', None) == 'user':
        return redirect('user_dashboard')
    if request.session.get('username', None) and request.session.get('type', None) == 'manager':
        return redirect('manager_dashboard')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(username=username) or User.objects.filter(email=email):
            messages.warning(request, "Account already exist, please Login to continue")
        else:
            password = request.POST['password']
            profile_pic = request.FILES.get('profile_pic', None)
            phone_number = request.POST['phone_number']
            error = []
            if (len(username) < 3):
                error.append(1)
                messages.warning(request, "Username Field must be greater than 3 character.")
            if (len(password) < 5):
                error.append(1)
                messages.warning(request, "Password Field must be greater than 5 character.")
            if (len(email) == 0):
                error.append(1)
                messages.warning(request, "Email field can't be empty")
            if (len(phone_number) != 10):
                error.append(1)
                messages.warning(request, "Valid Phone number is a 10 digit-integer.")
            if (len(error) == 0):
                password_hash = make_password(password)
                r_manager = User(username=username, password=password_hash, email=email, phone_number=phone_number,
                                 profile_pic=profile_pic)

                r_manager.save()
                messages.info(request, "Account Created Successfully, Please login to continue")
                redirect('manager_signup')
            else:
                redirect('login:manager-signup')

    else:
        redirect('login:user-signup')
    return render(request, 'login/manager_login.html', {})


def logout(request):
    if request.session.get('username', None):
        del request.session['username']
        del request.session['type']
        return render(request, "login/logout.html", {})
    else:
        return render(request, "login/user_login.html", {})
