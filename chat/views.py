from django.shortcuts import render
from chat.models import Room
from .models import TravelInfo
from rest_framework.decorators import api_view
from django.http import JsonResponse
from authentication.models import User
from .models import TravelInfo
import datetime as dt

from django.db.models import Q
import datetime as dt


def index_view(request):
    return render(
        request,
        "index.html",
        {
            "rooms": Room.objects.all(),
        }
    )


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(
        request,
        "room.html",
        {
            "room": chat_room,
        },
    )


@api_view(["GET"])
def register(request):
    if request.method == "POST":
        card_id = request.POST["card_id"]
        print(travel)
        return JsonResponse({"message": "here"})

    if request.method == "GET":
        card_id = request.GET["card_id"]
        user_check = User.objects.filter(card_id=card_id)
        if not user_check:
            return JsonResponse({"message": "User Not Found"})

        user = User.objects.get(card_id=card_id)
        if user:
            if user.is_onboard:
                # if true, user needs to offboard
                travel = TravelInfo.objects.get(
                    Q(user=user)
                    & (Q(dest_latitude_longitude=None) | Q(dest_latitude_longitude=""))
                )

                # User offboarded
                user.is_onboard = False
                user.save()

                dest_latitude = "Pul"
                dest_longitude = "chowk"
                distance_traveled = 0
                fare = 0
                dest_latitude_longitude_ = dest_latitude + dest_longitude
                if user.card_id == "A3E558A8":
                    dest_latitude_longitude_ = "Sundhara "
                    fare = 12.0

                travel.checkout_time = dt.datetime.now()
                travel.dest_latitude_longitude = dest_latitude_longitude_
                travel.distance_traveled = distance_traveled
                travel.fare = fare
                travel.save()

                return JsonResponse({"message": "Travel Information Updated"})
            else:
                user.is_onboard = True
                user.save()
                depart_latitude = "Pul"
                depart_longitude = "chowk"
                depart_latitude_longitude_ = depart_latitude + depart_longitude
                # user needs to onboard
                travel = TravelInfo.objects.create(
                    user=user,
                    bus_name="SajhaJaulakhelToBalaju",
                    depart_latitude_longitude=depart_latitude_longitude_,
                    checkin_time=dt.datetime.now(),
                    date=dt.datetime.today().date(),
                )

                return JsonResponse({"message": "Travel Information Created"})

        return JsonResponse({"message": "User Not Found"})
