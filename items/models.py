from django.db import models
import pandas as pd

from time import time

from users.models import User


start_time = time()
current_time = start_time
def log(message):
    global start_time
    global current_time
    new_time = time()
    print(f"{message}, {int(new_time - current_time)}s, total {int(new_time - start_time)}s")
    current_time = new_time


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


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    year = models.IntegerField(null=True)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=500,null=True)
    # poster_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=50, null=True, blank=True, unique=True)

    class Meta:
        ordering = ["-year"]
    def __str__(self):
        return self.name 

    @classmethod
    def import_from_csv(cls, csv_filename):
        #todo: add slugs and summarys to the csv
        df = pd.read_csv(csv_filename, sep="\t")
        n_items = df.shape[0]
        last_percentage = -1
        for i, row in df.iterrows():
            percentage = int(i * 100 / n_items)
            if percentage != last_percentage and percentage % 5 == 0:
                log(f"{percentage}% imported")
            last_percentage = percentage
            item_id = row["id"]
            # print(item_id, type(item_id))
            items_queryset = cls.objects.filter(pk=item_id)
            if items_queryset.exists():
                print(f"Found existing item with id {item_id}")
                continue

                item_entry = items_queryset.first()
                item_entry.delete()
            item_title = row["title"]
            item_year = int(row["year"].split('-')[0])
            item_author = row["author"]
            item_summary = f"A book written in {item_year} by {item_author}"
            item_slug = str(item_id)
            new_item = cls.objects.create(id=item_id,
                                          title=item_title,
                                          year=item_year,
                                          author=item_author,
                                          summary=item_summary,
                                          slug=item_slug)
            new_item.save()

    @classmethod 
    def clear_records(cls): # by adding cls we just enforce that it's a static method, proper to class
        cls.objects.all().delete()




class Rate(models.Model):
    user = models.ForeignKey(
        User, related_name='rates', on_delete=models.CASCADE)
    # item = models.ForeignKey(
    #     Movie, related_name='rates', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, related_name='rates', on_delete=models.CASCADE)
    score = models.IntegerField(primary_key=False)

    def __str__(self):
        return f"{self.user},{self.item},{self.score}"

    @classmethod
    def import_from_csv(cls, csv_filename):
        df = pd.read_csv(csv_filename)
        n_rates = df.shape[0]
        for i, row in df.iterrows():
            percentage = int(i * 100 / n_rates)
            if percentage % 5 == 0:
                log(f"{percentage}% imported")
            user_id = row["user"]
            users_queryset = User.objects.filter(pk=user_id)
            if users_queryset.exists():
                user_entry = users_queryset.first()
            else:
                print(f"no user with id {user_id}, skipping current entry")
                continue
            item_id = row["item"]
            items_queryset = Item.objects.filter(pk=item_id)
            if items_queryset.exists():
                item_entry = items_queryset.first()
            else:
                print(f"no item with id {item_id}, skipping current entry")
                continue
            score = row["rate"]
            new_rate = cls.objects.create(**{"user": user_entry, "item": item_entry, "score": score})
            new_rate.save()


    @classmethod 
    def clear_records(cls): # by adding cls we just enforce that it's a static method, proper to class
        cls.objects.all().delete()