from django.contrib import admin

from .models import Products, Categories, ProductImages, ProductSizes, Sizes


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand', 'name',)}
    list_display = ('brand', 'name', 'price', 'discount')
    list_editable = ('price', 'discount')
    search_fields = ('brand', 'name')
    list_filter = ('brand', 'price', 'category')
    fields = ('brand', 'name', 'category', 'slug', 'description', 'image', ('price', 'discount'))

@admin.register(ProductSizes)
class ProductSizesAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity')

admin.site.register(ProductImages)
admin.site.register(Sizes)
