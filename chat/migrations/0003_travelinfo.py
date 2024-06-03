# Generated by Django 3.2.23 on 2024-01-25 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_alter_message_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('depart_latitude_longitude', models.CharField(blank=True, max_length=100, null=True)),
                ('dest_latitude_longitude', models.CharField(blank=True, max_length=100, null=True)),
                ('distance_traveled', models.FloatField(blank=True, null=True)),
                ('fare', models.IntegerField(blank=True, null=True)),
                ('checkin_time', models.DateTimeField(blank=True, null=True)),
                ('checkout_time', models.DateTimeField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='TravelInfo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Travel Info',
                'verbose_name_plural': 'Travel Information',
            },
        ),
    ]