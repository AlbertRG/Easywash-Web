# Generated by Django 4.2.6 on 2023-11-13 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminpages', '0007_servicepage_hour_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceticket',
            name='car',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='adminpages.vehicle'),
        ),
        migrations.AddField(
            model_name='serviceticket',
            name='total',
            field=models.CharField(default='0', max_length=50),
        ),
        migrations.AlterField(
            model_name='serviceticket',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='serviceticket',
            name='paymethod',
            field=models.CharField(default='Efectivo', max_length=50),
        ),
    ]
