from rest_framework import serializers
from .models import TravelInfo
from authentication.serializers import UserSerializer

class TravelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelInfo
        fields = ('id','user', 'depart_latitude_longitude',
                  'dest_latitude_longitude','distance_traveled',
                  'fare','checkin_time','checkout_time',
                  'date')
