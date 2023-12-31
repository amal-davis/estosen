# Generated by Django 4.2.7 on 2024-01-04 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('estoapp', '0048_delete_order_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('pincode', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('email', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('product_name', models.CharField(blank=True, max_length=255)),
                ('quantity', models.CharField(blank=True, max_length=255)),
                ('size', models.CharField(blank=True, max_length=255)),
                ('total_price', models.CharField(blank=True, max_length=255)),
                ('product_image', models.URLField()),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
