from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart_add/', views.cart_add, name='cart_add'),
    path('cart_change_quantity/', views.cart_change_quantity, name='cart_change_quantity'),
    path('cart_change_size/', views.cart_change_size, name='cart_change_size'),
    path('cart_remove/', views.cart_remove, name='cart_remove'),
]
