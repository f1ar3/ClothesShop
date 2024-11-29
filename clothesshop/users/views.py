from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserLoginForm, UserRegistrationForm, ProfileForm, UserEditForm
from orders.models import Order, OrderItem

from .models import User


def cart(request):
    context = {
        'title': 'G-Shop | Cart',
    }
    return render(request, 'users/users_cart.html', context)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, you are now logged in")
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'G-Shop | Login',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f"{user.username}, you have successfully registered and logged into your account")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'G-Shop | Registration',
        'form': form
    }

    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.user.username}, you have successfully updated your profile")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': 'G-Shop | Profile',
        'form': form
    }

    return render(request, 'users/profile.html', context)


@login_required
def user_orders(request):
    orders = (
        Order.objects.filter(user=request.user).prefetch_related(Prefetch(
            'orderitem_set', queryset=OrderItem.objects.all()))
        .order_by('-id')
    )

    context = {
        'title': 'G-Shop | User Orders',
        'orders': orders
    }

    return render(request, 'users/user_orders.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    users = User.objects.all()

    context = {
        'users': users,
        'title': 'G-Shop | Users Management',
    }
    return render(request, 'users/manage_users.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Пользователь {user.username} успешно обновлен.")
            return redirect('users:manage_users')
        else:
            messages.error(request, "Ошибка при сохранении данных.")

    else:
        form = UserEditForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'users/edit_user.html', context)

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, you have successfully logged out")
    auth.logout(request)
    return redirect(reverse('main:index'))
