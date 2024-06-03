# Generated by Django 3.2.23 on 2024-01-25 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_travelinfo_bus_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TravelInfo', to=settings.AUTH_USER_MODEL),
        ),
    ]
