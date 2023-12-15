# Generated by Django 4.2.7 on 2023-12-10 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image_section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoapp.category')),
                ('images', models.ManyToManyField(blank=True, to='estoapp.image_section')),
            ],
        ),
    ]
