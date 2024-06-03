# Generated by Django 3.2.23 on 2024-01-25 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_is_onboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='user/profile/', verbose_name='Profile Picture'),
        ),
    ]