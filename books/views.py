from statistics import quantiles
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from books.models import Book, Catalog, Basket, BookOfTheMonth, Review
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

def index(request):

    all_books = Book.objects.all()

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    try:
        book_of_month_entry = BookOfTheMonth.objects.get(
            month=current_month,
            year=current_year,
            is_active=True
        )
        book_of_month = book_of_month_entry.book
        print(f"Найдена книга месяца: {book_of_month.title}")
    except BookOfTheMonth.DoesNotExist:
        print("Книга месяца на текущий месяц не найдена")
        book_of_month_entry = BookOfTheMonth.objects.filter(
            is_active=True
        ).order_by('-year', '-month').first()

        if book_of_month_entry:
            book_of_month = book_of_month_entry.book
            print(f"Найдена последняя активная книга месяца: {book_of_month.title}")
        else:
            book_of_month = None
            print("Активных книг месяца не найдено")

    popular_books = all_books.order_by('-id')[:8]

    if all_books.count() > 8:
        new_books = all_books.order_by('-id')[8:16]
    else:
        new_books = all_books[:4]

    if all_books.count() > 16:
        recommended_books = all_books[16:24]
    else:
        recommended_books = all_books[:4]

    if all_books.count() < 8:
        popular_books = all_books[:4]
        new_books = all_books[:4]
        recommended_books = all_books[:4]

    context = {
        'title': 'Litmarket',
        'popular_books': popular_books,
        'new_books': new_books,
        'recommended_books': recommended_books,
        'book_of_month': book_of_month,
    }

    return render(request, "books/index.html", context)

def books(request, category_id=None, page=1):
    sort_by = request.GET.get('sort', 'default')
    selected_genres = request.GET.getlist('genre')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_query = request.GET.get('search', '')

    category_param = request.GET.get('category')
    genre_param = request.GET.get('genre')
    category_name = request.GET.get('category_name')

    filtered_books = Book.objects.all()

    if category_param:
        filtered_books = filtered_books.filter(catalog_id=category_param)
    elif genre_param:
        filtered_books = filtered_books.filter(catalog_id=genre_param)
    elif category_id:
        filtered_books = filtered_books.filter(catalog_id=category_id)
    elif category_name:
        filtered_books = filtered_books.filter(catalog_id__category=category_name)

    if selected_genres:
        filtered_books = filtered_books.filter(catalog_id__id__in=selected_genres)

    if min_price:
        filtered_books = filtered_books.filter(price__gte=min_price)
    if max_price:
        filtered_books = filtered_books.filter(price__lte=max_price)

    if search_query:
        filtered_books = filtered_books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query)
        )

    if sort_by == 'title-asc':
        filtered_books = filtered_books.order_by('title')
    elif sort_by == 'title-desc':
        filtered_books = filtered_books.order_by('-title')
    elif sort_by == 'price-asc':
        filtered_books = filtered_books.order_by('price')
    elif sort_by == 'price-desc':
        filtered_books = filtered_books.order_by('-price')
    else:
        filtered_books = filtered_books.order_by('id')

    total_count = filtered_books.count()

    paginator = Paginator(filtered_books, 12)
    books_paginator = paginator.get_page(page)

    categories = Catalog.objects.all()
    unique_categories = categories.values('category').distinct()
    categories_with_genres = []

    for cat in unique_categories:
        genres = categories.filter(category=cat['category'])
        categories_with_genres.append({
            'category': cat['category'],
            'genres': genres
        })

    current_category_name = None
    current_genre_name = None

    if category_param:
        try:
            catalog = Catalog.objects.get(id=category_param)
            current_category_name = catalog.category
        except Catalog.DoesNotExist:
            pass
    elif genre_param:
        try:
            catalog = Catalog.objects.get(id=genre_param)
            current_genre_name = catalog.genre
        except Catalog.DoesNotExist:
            pass
    elif category_name:
        current_category_name = category_name

    current_params = request.GET.copy()
    if 'page' in current_params:
        current_params.pop('page')

    user_books_ids = []
    if request.user.is_authenticated:
        user_books_ids = request.user.my_books.values_list('book_id', flat=True)

    context = {
        'title': 'Litmarket | Каталог книг',
        'books': books_paginator,
        'categories': categories_with_genres,
        'all_categories': categories,
        'selected_genres': [str(id) for id in selected_genres],
        'min_price': min_price,
        'max_price': max_price,
        'search_query': search_query,
        'current_sort': sort_by,
        'total_count': total_count,
        'category_id': category_id,
        'current_category': category_param,
        'current_genre': genre_param,
        'current_category_name': current_category_name,
        'current_genre_name': current_genre_name,
        'current_params': current_params.urlencode(),
        'user_books_ids': list(user_books_ids),  # Добавлено
    }

    return render(request, "books/books.html", context)

@login_required
def basket_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    basket, created = Basket.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'quantity': 1}
    )

    if not created:
        basket.quantity += 1
        basket.save()
        messages.success(request, f'Количество книг "{book.title}" увеличено до {basket.quantity}')
    else:
        messages.success(request, f'Книга "{book.title}" добавлена в корзину')

    return redirect(request.META.get('HTTP_REFERER', 'books:index'))

@login_required
def basket_remove(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    remove_all = request.GET.get('remove') == 'all'

    baskets = Basket.objects.filter(user=request.user, book=book)

    if baskets.exists():
        basket = baskets.first()

        if remove_all:
            basket.delete()
            messages.success(request, f'Книга "{book.title}" полностью удалена из корзины')
        else:
            if basket.quantity > 1:
                basket.quantity -= 1
                basket.save()
                messages.success(request, f'Количество книг "{book.title}" уменьшено до {basket.quantity}')
            else:
                basket.delete()
                messages.success(request, f'Книга "{book.title}" удалена из корзины')
    else:
        messages.error(request, 'Товар не найден в корзине')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def basket_clear(request):
    if request.method == 'POST' or request.method == 'GET':
        count = Basket.objects.filter(user=request.user).count()
        Basket.objects.filter(user=request.user).delete()
        if count > 0:
            messages.success(request, f'Корзина успешно очищена. Удалено книг: {count}')
        else:
            messages.info(request, 'Корзина уже пуста')
    return redirect('users:basket')

def agreement(request):
    return render(request, 'books/agreement.html')

def card(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    categories = Catalog.objects.all()

    purchased_count = book.orderitem_set.filter(
        book=book,
        order__status__in=['delivered', 'confirmed']
    ).values('order__user').distinct().count()

    user_books_ids = []
    user_has_rated = False
    user_has_reviewed = False

    if request.user.is_authenticated:
        user_books_ids = request.user.my_books.values_list('book_id', flat=True)
        user_has_rated = Review.objects.filter(user=request.user, book=book, comment__isnull=True).exists()
        user_has_reviewed = Review.objects.filter(user=request.user, book=book, comment__isnull=False).exists()

    reviews = Review.objects.filter(book=book, comment__isnull=False).order_by('-created_at')

    context = {
        'book': book,
        'categories': categories,
        'title': book.title,
        'user_books_ids': list(user_books_ids),
        'purchased_count': purchased_count,
        'user_has_rated': user_has_rated,
        'user_has_reviewed': user_has_reviewed,
        'reviews': reviews,
    }
    return render(request, 'books/card.html', context)

@login_required
def rate_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    existing_review = Review.objects.filter(user=request.user, book=book, comment__isnull=True).first()
    if existing_review:
        messages.warning(request, 'Вы уже оценили эту книгу')
        return redirect('books:card', book_id=book_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')

        if rating and rating.isdigit() and 1 <= int(rating) <= 5:
            Review.objects.create(
                user=request.user,
                book=book,
                rating=int(rating),
                comment=None
            )
            messages.success(request, f'Спасибо за оценку! Вы оценили книгу на {rating} звезд.')
            return redirect('books:card', book_id=book_id)
        else:
            messages.error(request, 'Пожалуйста, выберите корректную оценку')

    context = {
        'book': book,
        'title': f'Оценить книгу - {book.title}',
    }
    return render(request, 'books/rate_book.html', context)

@login_required
def review_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        if not rating or not rating.isdigit() or not 1 <= int(rating) <= 5:
            messages.error(request, 'Пожалуйста, выберите корректную оценку')
        elif not comment:
            messages.error(request, 'Пожалуйста, напишите комментарий к отзыву')
        else:
            review, created = Review.objects.get_or_create(
                user=request.user,
                book=book,
                defaults={
                    'rating': int(rating),
                    'comment': comment
                }
            )

            if not created:
                review.rating = int(rating)
                review.comment = comment
                review.save()
                messages.success(request, 'Ваш отзыв был обновлен!')
            else:
                messages.success(request, 'Спасибо за ваш отзыв! Он поможет другим читателям.')

            return redirect('books:card', book_id=book_id)

    context = {
        'book': book,
        'title': f'Оставить отзыв - {book.title}',
    }
    return render(request, 'books/review_book.html', context)

def delivery_info(request):
    title = 'Оплата и доставка'
    content = {
        'title': title,
    }
    return render(request, 'books/delivery.html', content)


