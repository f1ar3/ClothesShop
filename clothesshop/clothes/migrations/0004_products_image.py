# Generated by Django 5.1.2 on 2024-11-04 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0003_alter_products_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='clothes_image', verbose_name='Image'),
        ),
    ]