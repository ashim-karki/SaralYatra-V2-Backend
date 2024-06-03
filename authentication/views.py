from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (CustomObtainPairSerializer,
                        UserSerializer,
                        RegisterUserSerializer,
                        GetSearchedUserSerializer)

from .models import User
from django.db.models import Q


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    parser_classes = [MultiPartParser,FormParser, JSONParser]
    queryset = get_user_model().objects.all().filter()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny(), ]
        return super(UserViewSet,self).get_permissions()

    def create(self, request, *args, **kwargs):
        register_serializer = RegisterUserSerializer(data=request.data)
        if register_serializer.is_valid():
            new_user = register_serializer.save()
            if new_user:
                return Response(register_serializer.data,status = status.HTTP_201_CREATED)


        return Response(register_serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class GetUserViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = GetSearchedUserSerializer

    def list(self,request,*args,**kwargs):
        query = request.GET.get('user')
        # query = query['user'] if 'user' in query else None
        if query is not None:
            lookups = Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
            queryset = self.filter_queryset(self.get_queryset().filter(lookups))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"detail":"No query received for search"})

