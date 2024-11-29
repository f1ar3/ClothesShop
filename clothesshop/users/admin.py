from django.contrib import admin

from .models import User
from orders.admin import OrderTabularAdmin

from cart.admin import CartTabularAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name' )

    inlines = (CartTabularAdmin, OrderTabularAdmin)
