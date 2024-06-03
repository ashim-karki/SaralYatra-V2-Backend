from builtins import staticmethod #like classmethod
from django.contrib.auth import get_user_model
from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login



class CustomObtainPairSerializer(TokenObtainPairSerializer):
    #takes the token
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name',
                'last_name',
                'username',
                'date_of_birth',
                'card_id',
                'user_type',
            )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,style={'input_type':'password'})
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True,label = 'Confirm Password')

    email = serializers.EmailField(validators=[
        UniqueValidator(
            queryset=get_user_model().objects.all(),
            message='This Email is already in use'
        )
    ])

    class Meta:
        model = get_user_model()
        fields = ('first_name',
                'last_name',
                'username',
                'date_of_birth',
                'card_id',
                'user_type',
                'email',
                'password',
                'confirm_password',
            )

        extra_kwargs ={
            'password':
            {'write_only':True},
            'uuid':
                {'read_only':True}
        }

    def validate(self, attrs):
        password = attrs['password']
        confirm_password = attrs['confirm_password']
        if password!=confirm_password:
            raise serializers.ValidationError(
                {
                    'password':"Error:The Passwords didn't match"
                }
            )
        return attrs

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        username = validated_data['username']
        date_of_birth = validated_data['date_of_birth'] if 'date_of_birth' in validated_data else None
        user_type = validated_data['user_type'] if 'user_type' in validated_data else "normal"
        card_id = validated_data['card_id']
        

        user = self.Meta.model(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                user_type= user_type,
                                username=username,
                                date_of_birth=date_of_birth,
                                card_id = card_id
                                )
        user.set_password(password)
        user.save()
        return user


class GetSearchedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","first_name","last_name")