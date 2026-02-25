from django.urls import path
from users.views import login, register, logout_view, profile, basket

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout_view/', logout_view, name='logout_view'),
    path('profile/', profile, name='profile'),
    path('basket/', basket, name='basket'),

]