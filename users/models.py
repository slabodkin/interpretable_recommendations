from django.db import models
from django.contrib.auth.models import AbstractUser
import pandas as pd

from time import time

from .managers import CustomUserManager

start_time = time()
current_time = start_time
def log(message):
    global start_time
    global current_time
    new_time = time()
    print(f"{message}, {int(new_time - current_time)}s, total {int(new_time - start_time)}s")
    current_time = new_time

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
            users_queryset = cls.objects.filter(email=record.get("email"))
            if users_queryset.exists():
                user = users_queryset.first()
                user.delete()
                print(f"email:{record.get('email')} already exists, deleting") 
            new_user = cls.objects.create(**record)
            new_user.is_active = True
            new_user.save()
            print("Import operation done successfully")

    @classmethod
    def import_from_csv(cls, csv_filename):
        df = pd.read_csv(csv_filename)
        n_users = df.shape[0]
        for i, row in df.iterrows():
            percentage = int(i * 100 / n_users)
            if percentage % 5 == 0:
                log(f"{percentage}% imported")
            user_id = row["id"]
            users_queryset = cls.objects.filter(pk=user_id)
            if users_queryset.exists():
                user_entry = users_queryset.first()
                user_entry.delete()
            user_email = row["email"]
            user_password = row["password"]
            user_name = row["name"]
            new_user = cls.objects.create(pk=user_id,
                                          email=user_email,
                                          password=user_password,
                                          name=user_name)
            new_user.is_active = True
            new_user.set_password(new_user.password)
            new_user.save()

            # print("Import operation done successfully")


    @classmethod 
    def clear_records(cls): # by adding cls we just enforce that it's a static method, proper to class
        cls.objects.all().delete()






 



