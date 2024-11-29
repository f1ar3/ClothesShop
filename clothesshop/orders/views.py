from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from cart.models import Cart
from .forms import OrderForm
from .models import Order, OrderItem
from clothes.models import ProductSizes


def order(request):
    if request.method == "POST":
        form = OrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            email=form.cleaned_data['email'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_by_card=form.cleaned_data['payment_by_card'],
                            order_price=cart_items.total_price(),
                        )

                        for item in cart_items:
                            product = item.product
                            name = item.product.name
                            price = item.product.sell_price()
                            size = item.size
                            quantity = item.quantity

                            product_sizes = ProductSizes.objects.filter(product=product, size=size).first()
                            if product_sizes.quantity < quantity:
                                raise ValidationError(
                                    f"There are only {product_sizes.quantity} of size {size} for product {product.brand} {product.name}")

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                                size=size,
                            )

                            product_sizes.quantity -= quantity
                            product_sizes.save()

                        cart_items.delete()

                        messages.success(request, "Order successfully created")
                        return redirect('user:user_orders')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('orders:order')
    else:

        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

        form = OrderForm(initial=initial)

    context = {
        'title': 'G-Shop | Order',
        'form': form,
    }

    return render(request, 'orders/order.html', context=context)

