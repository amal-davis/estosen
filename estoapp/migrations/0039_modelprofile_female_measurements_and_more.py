# Generated by Django 4.2.7 on 2024-01-01 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoapp', '0038_modelprofile_waistround'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelprofile',
            name='female_measurements',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='modelprofile',
            name='kid_boy_measurements',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='modelprofile',
            name='kid_girl_measurements',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='modelprofile',
            name='men_measurements',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
