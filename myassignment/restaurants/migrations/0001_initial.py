# Generated by Django 5.0.6 on 2024-12-08 12:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('rating', models.FloatField()),
                ('distance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='restaurants.restaurant')),
            ],
        ),
    ]