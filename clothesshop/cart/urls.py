from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('cart_add/<slug:product_slug>', views.cart_add, name='cart_add'),
    path('cart_remove/<int:cart_id>', views.cart_remove, name='cart_remove'),
]
