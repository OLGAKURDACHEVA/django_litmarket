from django.urls import path
from books.views import books, basket_add, agreement, card
from django.shortcuts import render
from . import views

app_name = 'books'

urlpatterns = [
    path('', books, name='index'),
    path('<int:category_id>', books, name='category'),
    path('page/<int:page>', books, name='page'),
    path('basket-add/<int:book_id>', basket_add, name='basket_add'),
    path('agreement/', agreement, name='agreement'),
    path('book/<int:book_id>/', views.card, name='card'),
    # path('basket-delete/<int:book_id>', basket-delete, name='basket-delete'),


]
