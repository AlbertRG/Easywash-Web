# Generated by Django 3.2.12 on 2023-09-20 05:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adminpages', '0006_auto_20230912_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicepage',
            name='hour_date',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]