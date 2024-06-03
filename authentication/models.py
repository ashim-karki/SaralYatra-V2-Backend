import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from .manager import UserManager
import datetime
class User(AbstractBaseUser,PermissionsMixin):
    user_types=[
        ("normal","normal"),
        ("student", "student"),
        ("old_age", "old_age")
    ]
    id = models.UUIDField(editable=False,unique=True,default=uuid.uuid4,primary_key=True)
    card_id = models.CharField(max_length = 30, unique=True, null=True)
    first_name = models.CharField(max_length=128,blank=True,null=True)
    last_name = models.CharField(max_length=128,blank=True,null=True)
    username = models.CharField(max_length=128)
    email = models.EmailField('Email Address',unique=True)
    date_of_birth = models.DateField(null=True,blank=True) 
    user_type = models.CharField(max_length=20,choices=user_types,default="normal")
    is_onboard = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    photo = models.ImageField("Profile Picture",blank=True,null=True,upload_to ='user/profile/')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username']
    objects = UserManager()


    def __str__(self):
        return str(self.first_name) + '-' + self.email
    
    def get_age(self):
        today = datetime.datetime.today().date()
        print(type(self.date_of_birth))
        c =  today.year - self.date_of_birth.year
        return c

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"