# Generated by Django 4.2.7 on 2024-01-04 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0045_order_section_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_section',
            name='user',
        ),
    ]
