from django.urls import path
from users.views import (login, register, logout_view, profile, basket, checkout, mybooks,
                         add_to_mybooks, remove_from_mybooks, move_to_cart, clear_mybooks, mybooks_count,
                         order_list, order_detail, order_repeat, order_review )

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout_view/', logout_view, name='logout_view'),
    path('profile/', profile, name='profile'),
    path('basket/', basket, name='basket'),
    path('checkout/', checkout, name='checkout'),
    path('mybooks/', mybooks, name='mybooks'),
    path('mybooks/add/<int:book_id>/', add_to_mybooks, name='add_to_mybooks'),
    path('mybooks/remove/<int:book_id>/', remove_from_mybooks, name='remove_from_mybooks'),
    path('mybooks/move-to-cart/<int:book_id>/', move_to_cart, name='move_to_cart'),
    path('mybooks/clear/', clear_mybooks, name='clear_mybooks'),
    path('api/mybooks/count/', mybooks_count, name='mybooks_count'),
    path('orders/', order_list, name='order_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/<int:order_id>/repeat/', order_repeat, name='order_repeat'),
    path('orders/<int:order_id>/review/', order_review, name='order_review'),

]