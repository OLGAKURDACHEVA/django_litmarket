from statistics import quantiles
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from books.models import Book, Catalog, Basket
from django.core.paginator import Paginator

def index(request):
    context = {
        'title': 'Litmarket | Книжный уголок',
    }
    return render(request, "books/index.html", context)

def books(request, category_id=None, page=1):
    context = {
        'title': 'Litmarket | Каталог книг',
        'categories': Catalog.objects.all(),
    }
    if category_id:
        filtered_books = Book.objects.filter(catalog_id=category_id)
    else:
        filtered_books = Book.objects.all()

    paginator = Paginator(filtered_books, 4)
    books_paginator = paginator.page(page)
    context['books'] = books_paginator


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
        basket.quantity +=1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def agreement(request):
    return render(request, 'books/agreement.html')