from django.db import models
from users.models import User

# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField(null=True)
    summary = models.TextField(max_length=500,null=True)
    poster_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=50, null=True, blank=True, unique=True)
    user = models.ForeignKey(
        User, related_name='items', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-year"]
    def __str__(self):
        return self.name 

    @classmethod
    def import_records(cls, record_list):
        for record in record_list:
            users_queryset = User.objects.filter(email=record.get("user"))
            if users_queryset.exists():
                user = users_queryset.first()
            else:
                print(f"no user with id {record.get('user')}, skipping movie {record.get('name')}")
                continue
            record["user"] = user
            new_movie = cls.objects.create(**record)
            new_movie.save()
            print("Import operation done successfully")

    @classmethod 
    def clear_records(cls): # by adding cls we just enforce that it's a static method, proper to class
        cls.objects.all().delete()
