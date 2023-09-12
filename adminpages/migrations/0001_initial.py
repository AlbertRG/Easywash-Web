# Generated by Django 3.2.12 on 2023-09-11 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=150)),
                ('quantity', models.IntegerField()),
                ('expirated', models.BooleanField()),
                ('expiration_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.CharField(max_length=7, unique=True)),
                ('model', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('color', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminpages.client')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('paymethod', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adminpages.client')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adminpages.service')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adminpages.vehicle'),
        ),
    ]
