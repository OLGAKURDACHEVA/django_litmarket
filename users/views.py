from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from books.models import Basket
from django.contrib.auth.decorators import login_required


def login(request):

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect('index')
    else:
        return redirect('index')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, message="Профиль обновлен успешно!")
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    baskets = Basket.objects.filter(user=request.user)
    total_quantity = sum(basket.quantity for basket in baskets)
    total_sum = sum(basket.sum() for basket in baskets)


    context = {'form': form, 'baskets': Basket.objects.filter(user=request.user),
               'total_quantity': total_quantity, 'total_sum': total_sum,
               }
    return render(request, 'users/profile.html', context)

def basket(request):
    return render(request, 'basket.html')



