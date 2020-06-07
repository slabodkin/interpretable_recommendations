import graphene
from items.models import Movie
from graphene_django.types import DjangoObjectType
from users.models import User
# from django.contrib.auth import get_user_model
import graphql_jwt


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


# class UserType(DjangoObjectType):
#     id = graphene.Int()
#     email = graphene.String()
#     name = graphene.String()
#     birthdate = graphene.types.datetime.Date()
#     gender = graphene.String()


#     class Meta:
#         model = User

#     def resolve_id(self, info):
#         return self.id
    
#     def resolve_email(self, info):
#         return self.email

#     def resolve_name(self, info):
#         return self.name

#     def resolve_birthdate(self, info):
#         return self.birthdate

#     def resolve_gender(self, info):
#         return self.gender
class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    movie_list = graphene.List(MovieType)
    movie = graphene.Field(MovieType, slug=graphene.String())
    user = graphene.Field(UserType, email=graphene.String())
    user_list = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_user_list(self, info):
        return User.objects.all()
    # userid_by_email = graphene.Field(UserType, email=graphene.String())

    def resolve_movie_list(self, info, *_):
        return Movie.objects.all().only("name", "poster_url", "slug")

    def resolve_movie(self, info, slug):
        movie_queryset = Movie.objects.all().filter(slug=slug)
        if movie_queryset.exists():
            return movie_queryset.first()

    #users
    def resolve_user(self, info, email):
        print("user_query: " + email)
        user_queryset = User.objects.all().filter(email=email)
        if user_queryset.exists():
            return user_queryset.first()

    def resolve_me(self, info):
        print("\n\nhi\n\n")
        print(info.context.user)
        print("\ndone\n")
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user


class SignupMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, email, password, name):
        user = User.objects.create(
            email=email
        )
        user.set_password(password)
        # user.set_name(name)
        user.name = name
        user.is_active = True
        user.save()

        return SignupMutation(user=user)


class Mutation(graphene.ObjectType):
    signup = SignupMutation.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
