from django import forms
from .models import Products, ProductImages


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['brand', 'name', 'description', 'image', 'price', 'discount', 'color', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price, RUB'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount, %'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['brand', 'name', 'description', 'image', 'price', 'discount', 'color', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price, RUB'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount, %'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = ProductImages
        fields = ['image']