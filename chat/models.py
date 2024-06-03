# from django.contrib.auth.models import User
import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
from asgiref.sync import async_to_sync
import json

from channels.layers import get_channel_layer

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()})"


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content} [{self.timestamp}]"


class TravelInfo(models.Model):
    id = models.UUIDField(
        editable=False, unique=True, default=uuid.uuid4, primary_key=True
    )
    user = models.ForeignKey(User, related_name="TravelInfo", on_delete=models.CASCADE)
    bus_name = models.CharField(max_length=100, null=True, blank=True)
    depart_latitude_longitude = models.CharField(max_length=100, blank=True, null=True)
    dest_latitude_longitude = models.CharField(max_length=100, blank=True, null=True)
    distance_traveled = models.FloatField(blank=True, null=True)
    fare = models.IntegerField(blank=True, null=True)
    checkin_time = models.DateTimeField(blank=True, null=True)
    checkout_time = models.DateTimeField(blank=True, null=True)
    date = models.DateField(("Date"), auto_now_add=True)

    class Meta:
        verbose_name = "Travel Info"
        verbose_name_plural = "Travel Information"

    def __str__(self):
        return str(self.user) + " at " + str(self.date)

    def save(self, *args, **kwargs):
        # print(self.user.id)
        channel_layer = get_channel_layer()
        user_obj = self.user
        # user_obj = User.objects.filter(id=self.user.id)
        group_name = "SajhaJaulakhelToBalaju"  # self.bus_name
        response_ = {
            "user_name": user_obj.get_full_name(),
            "age": user_obj.get_age(),
            "photo": self.user.photo.url,
            "onboard_status": self.user.is_onboard,
            "departure": self.depart_latitude_longitude,
        }

        if not self.user.is_onboard:
            response_.update(
                {
                    "fare": self.fare,
                    "distance_traveled": self.distance_traveled,
                    "destination": self.dest_latitude_longitude,
                }
            )
        async_to_sync(channel_layer.group_send)(
            group_name, {"type": "send_data", "value": json.dumps(response_)}
        )
        super(TravelInfo, self).save(*args, **kwargs)
