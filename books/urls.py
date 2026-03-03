from django.urls import path
from books.views import books, basket_add, agreement, card, basket_remove
from django.shortcuts import render


app_name = 'books'

urlpatterns = [
    path('', books, name='index'),
    path('category/<int:category_id>/', books, name='category'),
    path('page/<int:page>', books, name='page'),
    path('basket-add/<int:book_id>', basket_add, name='basket_add'),
    path('agreement/', agreement, name='agreement'),
    path('book/<int:book_id>/', card, name='card'),
    path('basket-remove/<int:book_id>', basket_remove, name='basket_remove'),

]
