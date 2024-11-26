from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import ProductsForm, ProductEditForm
from .models import Products, ProductImages, ProductSizes
from .utils import q_search


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all-products':
        products = Products.objects.all()
    elif query:
        products = q_search(query)
    elif category_slug == None:
        products = Products.objects.all()
        category_slug = 'all-products'
    else:
        products = Products.objects.filter(category__slug=category_slug)

    if on_sale:
        products = products.filter(discount__gt=0)

    if order_by and order_by != 'default':
        products = products.order_by(order_by)

    form = ProductsForm()
    paginator = Paginator(products, 4)
    current_page = paginator.page(page)

    context = {
        'title': 'G-Shop | Catalog',
        'products': current_page,
        'slug_url': category_slug,
        'form': form,
    }

    return render(request, 'clothes/catalog.html', context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    sizes = ProductSizes.objects.filter(product=product)
    form = ProductEditForm(instance=product)

    context = {
        'title': 'G-Shop | Product',
        'product': product,
        'sizes': sizes,
        'form': form,
    }

    return render(request, 'clothes/product.html', context=context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:catalog')
        else:
            form = ProductsForm()

    context = {
        'title': 'G-Shop | Add Product',
        'form': form,
    }

    return redirect('catalog:catalog', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            if request.FILES.getlist('new_images'):
                for image in request.FILES.getlist('new_images'):
                    ProductImages.objects.create(product=product, image=image)
            return redirect('catalog:product', product_slug)
    else:
        form = ProductEditForm(instance=product)

    context = {
        'title': 'G-Shop | Edit Product',
        'form': form,
        'product': product,
    }

    return render('catalog:product', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product "{product.name}" deleted successfully')
        return redirect('catalog:catalog')