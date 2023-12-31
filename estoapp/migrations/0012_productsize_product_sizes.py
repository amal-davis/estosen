# Generated by Django 4.2.5 on 2023-12-21 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0011_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='estoapp.productsize'),
        ),
    ]
