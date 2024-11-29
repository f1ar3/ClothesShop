from django.contrib import admin

from .models import Order, OrderItem


class OrderItemTabularAdmin(admin.TabularInline):
    model = OrderItem
    fields = 'product', 'name', 'price', 'quantity'
    search_fields = ['product', 'name', ]
    extra = 0


class OrderTabularAdmin(admin.TabularInline):
    model = Order
    fields = (
        "express_delivery",
        "status",
        "payment_by_card",
        "is_paid",
        "created_timestamp",
    )

    search_fields = (
        "express_delivery",
        "payment_by_card",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'order_price',
        'express_delivery',
        'payment_by_card',
        'is_paid',
        'created_timestamp',
    )

    search_fields = (
        'id',
        'user',
    )

    readonly_fields = ('created_timestamp',)

    list_filter = (
        'status',
        'express_delivery',
        'payment_by_card',
        'is_paid',
    )

    inlines = (OrderItemTabularAdmin,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'size', 'price', 'quantity')
    search_fields = (
        'order',
        'product',
        'name',
    )
