from django.contrib import admin

from .models import Products, Categories, ProductImages, Sizes, ProductSizes


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand', 'name',)}


admin.site.register(ProductImages)
admin.site.register(Sizes)
admin.site.register(ProductSizes)
