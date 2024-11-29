from django.contrib import admin

from .models import Cart


class CartTabularAdmin(admin.TabularInline):
    model = Cart
    fields = 'product', 'quantity', 'created_time'
    search_fields = 'product', 'quantity'
    readonly_fields = ('created_time',)
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'size', 'created_time')
    list_filter = ('user', 'product', 'created_time')