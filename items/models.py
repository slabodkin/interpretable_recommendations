from django.db import models
from users.models import User
import pandas as pd

# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField(null=True)
    summary = models.TextField(max_length=500,null=True)
    poster_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=50, null=True, blank=True, unique=True)

    class Meta:
        ordering = ["-year"]
    def __str__(self):
        return self.name 

    @classmethod
    def import_records(cls, record_list):
        for record in record_list:
            # users_queryset = User.objects.filter(email=record.get("user"))
            # if users_queryset.exists():
            #     user = users_queryset.first()
            # else:
            #     print(f"no user with id {record.get('user')}, skipping movie {record.get('name')}")
            #     continue
            # record["user"] = user
            movies_queryset = Movie.objects.filter(slug=record.get("slug"))
            if movies_queryset.exists():
                movie = movies_queryset.first()
                movie.delete()
                print(f"Name:{record.get('name')} already exists, deleting") 
            new_movie = cls.objects.create(**record)
            new_movie.save()
            print("Import operation done successfully")

    @classmethod 
    def clear_records(cls): # by adding cls we just enforce that it's a static method, proper to class
        cls.objects.all().delete()


class Rate(models.Model):
    user = models.ForeignKey(
        User, related_name='rates', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Movie, related_name='rates', on_delete=models.CASCADE)
    rate = models.IntegerField(primary_key=False)

    def __str__(self):
        return f"{self.user},{self.item},{self.rate}"

    @classmethod
    def import_records(cls, input_csv_filename):
        df = pd.read_csv(input_csv_filename)
        for i, row in df.iterrows():
            # print(row.user)
            # return
            user_email = row.user
            users_queryset = User.objects.filter(email=user_email)
            if users_queryset.exists():
                user_entry = users_queryset.first()
            else:
                print(f"no user with id {user_email}, skipping current entry")
                continue
            item_slug = row["item"]
            movies_queryset = Movie.objects.filter(slug=item_slug)
            if movies_queryset.exists():
                movie_entry = movies_queryset.first()
            else:
                print(f"no movie with id {item_slug}, skipping current entry")
                continue
            rate = row.rate
            new_rate = cls.objects.create(**{"user": user_entry, "item": movie_entry, "rate": rate})
            new_rate.save()
            print("Import operation done successfully")


    @classmethod 
    def clear_records(cls): # by adding cls we just enforce that it's a static method, proper to class
        cls.objects.all().delete()