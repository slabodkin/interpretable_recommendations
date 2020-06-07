from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

# Create your models here.
# class User(models.Model):
#     GENDER_CHOICES = [("male", "male"),
#                       ("female", "female"),
#                       ("other", "other")]

#     id = models.IntegerField(primary_key=True)
#     email = models.CharField(max_length=100, default="_")
#     name = models.CharField(max_length=100)
#     birthdate = models.DateField()
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=GENDER_CHOICES[-1][0])

#     class Meta:
#         ordering = ["id"]

#     def __str__(self):
#         return self.name 

#     @classmethod
#     #TODO: define import from csv (e.g. using pandas)
#     def import_records(cls, record_list):
#         for record in record_list:
#             users_queryset = User.objects.filter(id=record.get("id"))
#             if users_queryset.exists():
#                 user = users_queryset.first()
#                 user.delete()
#                 print(f"Id:{record.get('id')} already exists, deleting") 
#             new_user = cls.objects.create(**record)
#             print("Import operation done successfully")


class User(AbstractUser):
    GENDER_CHOICES = [("male", "male"),
                      ("female", "female"),
                      ("other", "other")]
    username = None
    email = models.EmailField(('email address'), unique=True)
    name = models.CharField(max_length=100)
    birthdate = models.DateField(default="2000-01-01")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=GENDER_CHOICES[-1][0])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @classmethod
    #TODO: define import from csv (e.g. using pandas)
    def import_records(cls, record_list):
        for record in record_list:
            users_queryset = User.objects.filter(email=record.get("email"))
            if users_queryset.exists():
                user = users_queryset.first()
                user.delete()
                print(f"Id:{record.get('id')} already exists, deleting") 
            new_user = cls.objects.create(**record)
            new_user.is_active = True
            print("Import operation done successfully")