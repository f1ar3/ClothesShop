from django.db import models
from django.utils.text import slugify


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Products(models.Model):
    brand = models.CharField(max_length=150, unique=False, verbose_name='Brand')
    name = models.CharField(max_length=150, unique=True, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    image = models.ImageField(upload_to='clothes_images', blank=True, null=True, verbose_name='Image')
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0, verbose_name='Price')
    discount = models.DecimalField(default=0, max_digits=2, decimal_places=0, verbose_name='Discount, %')
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Color')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Category')

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['brand']

    def __str__(self):
        return f"{self.brand} {self.name}"

    def display_id(self):
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f'{self.brand}-{self.name}')
            slug = base_slug
            counter = 1
            while Products.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class ProductImages(models.Model):
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Product', related_name='images')
    image = models.ImageField(upload_to='clothes_images', blank=True, null=True, verbose_name='Image')

    class Meta:
        db_table = 'product_image'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f"Image for {self.product.brand} {self.product.name}"


class Sizes(models.Model):
    size = models.CharField(max_length=10, unique=True, verbose_name='Size')

    class Meta:
        db_table = 'size'
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return f"{self.size}"

class ProductSizes(models.Model):
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Product', related_name='sizes')
    size = models.ForeignKey(to=Sizes, on_delete=models.CASCADE, verbose_name='Size', related_name='products')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')

    class Meta:
        db_table = 'product_size'
        verbose_name = 'Product Size'
        verbose_name_plural = 'Product Sizes'
        ordering = ['id']

    def __str__(self):
        return f"{self.product.name} {self.size} {self.quantity}"
