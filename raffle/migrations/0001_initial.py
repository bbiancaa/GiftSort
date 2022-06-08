# Generated by Django 4.0.4 on 2022-06-08 00:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryGift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observation')),
                ('host', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='raffle.categorygift')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name of Room')),
                ('link', models.CharField(max_length=100)),
                ('min_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Minimum value')),
                ('max_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Maximum value')),
                ('participant', models.ManyToManyField(to='raffle.participant')),
            ],
        ),
    ]