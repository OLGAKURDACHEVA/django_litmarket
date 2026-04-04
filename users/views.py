from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import logout
from books.models import Book, Basket, MyBooks, Order, OrderItem, Review
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator


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

@login_required
def basket(request):
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)
        total_sum = sum(basket.sum() for basket in baskets)
        total_quantity = sum(basket.quantity for basket in baskets)
    else:
        baskets = []
        total_sum = 0
        total_quantity = 0

    context = {
        'baskets': baskets,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
    }
    return render(request, 'users/basket.html', context)

@login_required
def checkout(request):
    baskets = Basket.objects.filter(user=request.user)
    if not baskets.exists():
        return redirect('books:index')

    total_sum = sum(basket.sum() for basket in baskets)
    total_quantity = baskets.count()

    if request.method == 'POST':
        pickup_point = request.POST.get('pickup_point')
        payment_method = request.POST.get('payment_method')
        comment = request.POST.get('comment', '')
        order = Order.objects.create(
            user=request.user,
            total_sum=total_sum,
            pickup_point=pickup_point,
            payment_method=payment_method,
            comment=comment
        )
        for basket in baskets:
            OrderItem.objects.create(
                order=order,
                book=basket.book,
                quantity=basket.quantity,
                price=basket.book.price
            )
        baskets.delete()
        messages.success(request, f'Заказ № {order.order_number} успешно оформлен!')
        return redirect('users:order_list')

    context = {
        'baskets': baskets,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
    }
    return render(request, 'users/checkout.html', context)

def mybooks(request):
    my_books = MyBooks.objects.filter(user=request.user).select_related('book', 'book__author')
    context = {
        'my_books': [item.book for item in my_books],
        'title': 'Мои книги',
    }
    return render(request, 'users/mybooks.html', context)

@login_required
def add_to_mybooks(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    MyBooks.objects.get_or_create(user=request.user, book=book)
    return redirect(request.META.get('HTTP_REFERER', 'books:index'))

@login_required
def remove_from_mybooks(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    MyBooks.objects.filter(user=request.user, book=book).delete()
    messages.success(request, f'Книга "{book.title}" удалена из Моих книг')
    return redirect(request.META.get('HTTP_REFERER', 'books:index'))

@login_required
def toggle_mybooks(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    my_book, created = MyBooks.objects.get_or_create(user=request.user, book=book)

    if not created:
        my_book.delete()

    return redirect(request.META.get('HTTP_REFERER', 'books:index'))

@login_required
def move_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)



    basket, created = Basket.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}
    )
    if not created:
        basket.quantity += 1
        basket.save()
        messages.success(request, f'Количество книги "{book.title}" в корзине увеличено до {basket.quantity}')
    else:
        messages.success(request, f'Книга "{book.title}" перемещена в корзину')

    return redirect('users:mybooks')

@login_required
def clear_mybooks(request):
    count = MyBooks.objects.filter(user=request.user).count()
    MyBooks.objects.filter(user=request.user).delete()
    messages.success(request, f'Все книги ({count}) удалены из Моих книг')
    return redirect('users:mybooks')

@login_required
def mybooks_count(request):
    count = MyBooks.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    status = request.GET.get('status')
    if status and status != 'all':
        orders = orders.filter(status=status)

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'orders': page_obj,
        'current_status': status or 'all',
    }
    return render(request, 'users/order_list.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order
    }
    return render(request, 'users/order_detail.html', context)

@login_required
def order_repeat(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)

        for item in order.items.all():
            basket, created = Basket.objects.get_or_create(
                user=request.user,
                book=item.book,
                defaults={'quantity': item.quantity}
            )
            if not created:
                basket.quantity += item.quantity
                basket.save()

        messages.success(request, f'Товары из заказа №{order.order_number} добавлены в корзину')

    return redirect('users:basket')

@login_required
def order_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='delivered')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            user=request.user,
            book=order.items.first().book,
            rating=rating,
            comment=comment
        )

        messages.success(request, 'Спасибо за ваш отзыв!')
        return redirect('users:order_list')

    context = {
        'order': order
    }
    return render(request, 'users/review_form.html', context)
