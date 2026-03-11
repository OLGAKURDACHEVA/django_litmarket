from django.urls import path
from books.views import books, basket_add, agreement, card, basket_remove, delivery_info, basket_clear, loyalty_program, loyalty_rules, certificates, certificate_rules
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
    path('delivery/', delivery_info, name='delivery'),
    path('basket/clear/', basket_clear, name='basket_clear'),
    path('loyalty/', loyalty_program, name='loyalty'),
    path('loyalty/rules/', loyalty_rules, name='loyalty_rules'),
    path('certificates/', certificates, name='certificates'),
    path('certificate_rules/', certificate_rules, name='certificate_rules'),

]
