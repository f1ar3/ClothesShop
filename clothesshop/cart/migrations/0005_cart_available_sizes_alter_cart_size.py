# Generated by Django 5.1.2 on 2024-11-27 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_cart_available_sizes_alter_cart_size'),
        ('clothes', '0011_sizes_alter_productsizes_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='available_sizes',
            field=models.ManyToManyField(related_name='available_sizes', to='clothes.sizes', verbose_name='Available Sizes'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_size', to='clothes.sizes', verbose_name='Size'),
        ),
    ]