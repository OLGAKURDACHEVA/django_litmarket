from statistics import quantiles
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from books.models import Book, Catalog, Basket
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages


def index(request):
    context = {
        'title': 'Litmarket | Книжный уголок',
    }
    return render(request, "books/index.html", context)

def books(request, category_id=None, page=1):
    sort_by = request.GET.get('sort', 'default')
    selected_genres = request.GET.getlist('genre')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_query = request.GET.get('search', '')

    if category_id:
        filtered_books = Book.objects.filter(catalog_id=category_id)
    else:
        filtered_books = Book.objects.all()

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
    }

    return render(request, "books/books.html", context)

@login_required
def basket_add(request, book_id):
    book = Book.objects.get(id=book_id)
    baskets = Basket.objects.filter(user=request.user, book=book)

    if not baskets.exists():
        Basket.objects.create(user=request.user, book=book)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    baskets = Basket.objects.filter(user=request.user, book=book)

    if baskets.exists():
        basket = baskets.first()
        if basket.quantity > 1:
            basket.quantity -= 1
            basket.save()
        else:
            basket.delete()
    else:
        messages.error(request, 'Товар не найден в корзине')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def agreement(request):
    return render(request, 'books/agreement.html')

def card(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    categories = Catalog.objects.all()

    context = {
        'book': book,
        'categories': categories,
        'title': book.title,
    }
    return render(request, 'books/card.html', context)
