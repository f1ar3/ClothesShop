from django.contrib.messages.context_processors import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect

from cart.models import Cart
from .forms import OrderForm
from .models import Order, OrderItem


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
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )

                        for item in cart_items:
                            product = item.product
                            name = item.product.name
                            price = item.product.sell_price()
                            size = item.size
                            quantity = item.quantity

                        if product.quantity > 0:
                            raise ValidationError("This product is not available")

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                            size=size,
                        )

                        product.quantity -= quantity
                        product.save()

                    cart_items.delete()

                    messages.success(request, "Order successfully created")
                    return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('cart:order')
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