# Generated by Django 4.2.7 on 2024-01-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0055_order_sections_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_sections',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
