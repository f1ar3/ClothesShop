from django.db import models

from clothes.models import Products, Sizes
from users.models import User


class CartQuerySet(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

    def total_price_with_delivery(self):
        return sum(cart.products_price() for cart in self)

class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='User')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')
    size = models.ForeignKey(to=Sizes, on_delete=models.CASCADE, verbose_name='Size', related_name='cart_size')
    available_sizes = models.ManyToManyField(to=Sizes, verbose_name='Available Sizes', related_name='available_sizes')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Date added')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ['-id']

    objects = CartQuerySet.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f'Cart of user {self.user.username} | Product: {self.product.brand} {self.product.name} | Quantity: {self.quantity}'





