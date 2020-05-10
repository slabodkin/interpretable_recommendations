import graphene
from items.models import Movie
from users.models import User
from graphene_django.types import DjangoObjectType


class MovieType(DjangoObjectType):
    id = graphene.Int()
    name = graphene.String()
    year = graphene.Int()
    summary = graphene.String()
    poster_url = graphene.String()
    slug = graphene.String()

    class Meta:
        model = Movie

    def resolve_id(self, info):
        return self.id
    
    def resolve_name(self, info):
        return self.name

    def resolve_year(self, info):
        return self.year

    def resolve_summary(self, info):
        return self.summary

    def resolve_poster_url(self, info):
        # Note: in client side app snake_case fields
        # will be resolved as camelCase
        # Eg: poster_url ==> posterUrl
        return self.poster_url

    def resolve_slug(self, info):
        return self.slug


class UserType(DjangoObjectType):
    id = graphene.Int()
    name = graphene.String()
    birthdate = graphene.types.datetime.Date()
    gender = graphene.String(   )

    class Meta:
        model = User

    def resolve_id(self, info):
        return self.id
    
    def resolve_name(self, info):
        return self.name

    def resolve_birthdate(self, info):
        return self.birthdate

    def resolve_gender(self, info):
        return self.gender


class Query(graphene.ObjectType):
    movie_list = graphene.List(MovieType)
    movie = graphene.Field(MovieType, slug=graphene.String())
    user = graphene.Field(UserType, user_id=graphene.Int())

    def resolve_movie_list(self, info, *_):
        return Movie.objects.all().only("name", "poster_url", "slug")

    def resolve_movie(self, info, slug):
        movie_queryset = Movie.objects.all().filter(slug=slug)
        if movie_queryset.exists():
            return movie_queryset.first()

    #users
    def resolve_user(self, info, user_id):
        user_queryset = User.objects.all().filter(id=user_id)
        if user_queryset.exists():
            return user_queryset.first()

schema = graphene.Schema(query=Query)
