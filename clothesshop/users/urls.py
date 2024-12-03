from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('statistics/', views.statistics, name='statistics'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('logout/', views.logout, name='logout'),
]