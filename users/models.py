from django.db import models

# Create your models here.
class User(models.Model):
    GENDER_CHOICES = [("male", "male"),
                      ("female", "female"),
                      ("other", "other")]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=GENDER_CHOICES[-1][0])

    # year = models.IntegerField(null=True)
    # summary = models.TextField(max_length=500,null=True)
    # poster_url = models.URLField(blank=True, null=True)
    # slug = models.SlugField(max_length=50, null=True, blank=True, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name 

    @classmethod
    #TODO: define import from csv (e.g. using pandas)
    def import_records(cls, record_list):
        for record in record_list:
            users_queryset = User.objects.filter(id=record.get("id"))
            if users_queryset.exists():
                user = users_queryset.first()
                user.delete()
                print(f"Id:{record.get('id')} already exists, deleting") 
            new_user = cls.objects.create(**record)
            print("Import operation done successfully")

