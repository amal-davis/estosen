# Generated by Django 4.2.7 on 2023-12-22 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0015_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
