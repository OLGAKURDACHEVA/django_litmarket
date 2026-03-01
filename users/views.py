from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import logout
from books.models import Basket, MyBooks, Book
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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

@login_required
def checkout(request):
    baskets = Basket.objects.filter(user=request.user)
    if not baskets.exists():
        return redirect('books:index')

    total_sum = sum(basket.sum() for basket in baskets)
    total_quantity = baskets.count()

    context = {
        'baskets': baskets,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
    }
    return render(request, 'users/checkout.html', context)


def mybooks(request):
    """Страница Мои книги"""
    my_books = MyBooks.objects.filter(user=request.user).select_related('book', 'book__author')
    context = {
        'my_books': [item.book for item in my_books],
        'title': 'Мои книги',
    }
    return render(request, 'users/mybooks.html', context)


@login_required
def add_to_mybooks(request, book_id):
    """Добавление книги в Мои книги"""
    book = get_object_or_404(Book, id=book_id)
    MyBooks.objects.get_or_create(user=request.user, book=book)
    return redirect(request.META.get('HTTP_REFERER', 'books:index'))


@login_required
def remove_from_mybooks(request, book_id):
    """Удаление книги из Мои книги"""
    book = get_object_or_404(Book, id=book_id)
    MyBooks.objects.filter(user=request.user, book=book).delete()
    return redirect('users:mybooks')  # указываем users:mybooks


@login_required
def move_to_cart(request, book_id):
    """Перемещение книги из Мои книги в корзину"""
    book = get_object_or_404(Book, id=book_id)

    # Удаляем из Мои книги
    MyBooks.objects.filter(user=request.user, book=book).delete()

    # Добавляем в корзину
    basket, created = Basket.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}
    )
    if not created:
        basket.quantity += 1
        basket.save()

    return redirect('users:mybooks')


@login_required
def clear_mybooks(request):
    """Очистка всех книг из Мои книги"""
    MyBooks.objects.filter(user=request.user).delete()
    return redirect('users:mybooks')


@login_required
def mybooks_count(request):
    """API для получения количества книг в Мои книги"""
    count = MyBooks.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})
