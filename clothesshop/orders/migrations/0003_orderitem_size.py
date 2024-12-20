# Generated by Django 5.1.2 on 2024-11-28 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0012_alter_sizes_options_alter_sizes_table'),
        ('orders', '0002_remove_order_payment_on_get_order_payment_by_card_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='clothes.sizes', verbose_name='Size'),
        ),
    ]
