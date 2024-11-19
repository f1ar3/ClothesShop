from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<slug:product_slug>', views.edit_product, name='edit_product'),
    path('delete_product/<slug:product_slug>', views.delete_product, name='delete_product'),
    path('search/', views.catalog, name='search'),
    path('<slug:category_slug>/', views.catalog, name='catalog_by_category'),
    path('product/<slug:product_slug>', views.product, name='product'),
]
