# Generated by Django 4.2.6 on 2023-11-15 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminpages', '0010_service_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='brand',
            field=models.CharField(default='Nissan', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='serviceticket',
            name='car',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminpages.vehicle'),
        ),
    ]
