# Generated by Django 4.2.5 on 2023-12-21 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0012_productsize_product_sizes'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='estoapp.productsize'),
        ),
    ]
