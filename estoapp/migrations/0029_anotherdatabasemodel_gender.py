# Generated by Django 4.2.7 on 2023-12-31 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0028_anotherdatabasemodel_age_anotherdatabasemodel_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='anotherdatabasemodel',
            name='gender',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
