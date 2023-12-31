# Generated by Django 4.2.7 on 2023-12-10 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0002_image_section_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(default='In stock', max_length=20),
        ),
    ]
