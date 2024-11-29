from django.http import JsonResponse

from django.template.loader import render_to_string

from .models import Cart
from .utils import get_user_carts
from clothes.models import ProductSizes, Products, Sizes

def cart_add(request):
    product_id = request.POST.get('product_id')
    product = Products.objects.get(id=product_id)
    size_char = request.POST.get('size')
    print(size_char)
    size = Sizes.objects.get(size=size_char)
    available_sizes = ProductSizes.objects.filter(product_id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            cart = Cart.objects.create(user=request.user, product=product, quantity=1, size=size)
            available_sizes_list = [product_size.size for product_size in available_sizes]
            cart.available_sizes.set(available_sizes_list)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string('cart/cart.html', {'carts': user_cart}, request=request)

    response_data = {
        'message': 'Product added to cart.',
        'cart_items_html': cart_items_html,
    }

    return JsonResponse(response_data)


def cart_change_quantity(request):
    cart_id = request.POST.get('cart_id')
    quantity = request.POST.get('quantity')

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity

    cart.save()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string('cart/cart.html', {'carts': user_cart}, request=request)

    response_data = {
        'cart_items_html': cart_items_html,
        'quantity': cart.quantity,
    }

    return JsonResponse(response_data)


def cart_change_size(request):
    cart_id = request.POST.get('cart_id')
    size_id = request.POST.get('size')
    print(size_id)

    size = Sizes.objects.get(id=size_id)

    cart = Cart.objects.get(id=cart_id)

    cart.size = size

    cart.save()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string('cart/cart.html', {'carts': user_cart}, request=request)

    response_data = {
        'cart_items_html': cart_items_html,
        'size': cart.size.size,
    }

    return JsonResponse(response_data)


def cart_change_delivery(request):
    user_cart = get_user_carts(request)

    products_price = user_cart.total_price()
    delivery_type = request.POST.get('delivery_type')

    if delivery_type == 'express':
        delivery_price = 500
    else:
        delivery_price = 0

    total_price = products_price + delivery_price
    user_cart.total_price_with_delivery = total_price

    cart_html = render_to_string('cart/cart.html', {'carts': user_cart, 'delivery_type': delivery_type, 'delivery_price': delivery_price,}, request=request)

    response_data = {
        'delivery_type': delivery_type,
        'cart_html': cart_html,
        'delivery_price': delivery_price,
        'total_price': user_cart.total_price_with_delivery,
    }

    return JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get('cart_id')

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string('cart/cart.html', {'carts': user_cart}, request=request)

    response_data = {
        'message': 'Product removed from cart.',
        'cart_items_html': cart_items_html,
        'quantity_deleted' : quantity,
    }

    return JsonResponse(response_data)
