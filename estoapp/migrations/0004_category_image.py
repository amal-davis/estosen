# Generated by Django 4.2.7 on 2023-12-15 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0003_product_quantity_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]
