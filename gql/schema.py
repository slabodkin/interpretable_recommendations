import graphene
from items.models import Movie, Item, Rate
from graphene_django.types import DjangoObjectType
from users.models import User
# from django.contrib.auth import get_user_model
import graphql_jwt
from graphql_jwt.shortcuts import get_token
from recommendations.recommender import recommend_for_user
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


class MovieType(DjangoObjectType):
    id = graphene.Int()
    name = graphene.String()
    year = graphene.Int()
    summary = graphene.String()
    poster_url = graphene.String()
    slug = graphene.String()
    # user = graphene.Field(UserType)

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

class ItemType(DjangoObjectType):
    id = graphene.Int()
    title = graphene.String()
    year = graphene.Int()
    author = graphene.String()
    summary = graphene.String()
    slug = graphene.String()

    class Meta:
        model = Item

    def resolve_id(self, info):
        return self.id
    
    def resolve_title(self, info):
        return self.title

    def resolve_year(self, info):
        return self.year

    def resolve_author(self, info):
        return self.author

    def resolve_summary(self, info):
        return self.summary

    def resolve_slug(self, info):
        return self.slug

    # def resolve_user(self, info):
    #     return self.user

class RateType(DjangoObjectType):
    user = graphene.Field(UserType)
    item = graphene.Field(ItemType)
    score = graphene.Int()

    class Meta:
        model = Rate

    def resolve_user(self, info):
        return self.user
    
    def resolve_item(self, info):
        return self.item
    
    def resolve_score(self, info):
        return self.score


class Query(graphene.ObjectType):
    # movie_list = graphene.List(MovieType)
    # movie = graphene.Field(MovieType, slug=graphene.String())
    item_list = graphene.List(ItemType, n=graphene.Int())
    item = graphene.Field(ItemType, item_id=graphene.Int())
    user = graphene.Field(UserType, email=graphene.String())
    rate = graphene.Field(RateType, user_email=graphene.String(), item_slug=graphene.String())
    user_list = graphene.List(UserType)
    me = graphene.Field(UserType)
    # recommendations = graphene.List(MovieType)
    recommendations = graphene.List(ItemType)

    def resolve_user_list(self, info):
        return User.objects.all()

    # def resolve_movie_list(self, info, *_):
    #     return Movie.objects.all().only("name", "poster_url", "slug")

    # def resolve_movie(self, info, slug):
    #     movie_queryset = Movie.objects.all().filter(slug=slug)
    #     if movie_queryset.exists():
    #         return movie_queryset.first()

    def resolve_item_list(self, info, n):
        return Item.objects.all().order_by('?')[:n]#.only("name", "poster_url", "slug")

    def resolve_item(self, info, item_id):
        item_queryset = Item.objects.all().filter(pk=item_id)
        if item_queryset.exists():
            return item_queryset.first()

    # def resolve_rate(self, info, user_email, item_slug):
    #     movie_queryset = Movie.objects.all().filter(slug=item_slug)
    #     if movie_queryset.exists():
    #         rate_movie = movie_queryset.first()
    #     user_queryset = User.objects.all().filter(email=user_email)
    #     if user_queryset.exists():
    #         rate_user = user_queryset.first()
    #     if rate_movie is not None and user_email is not None:
    #         rate_queryset = Rate.objects.all().filter(user=rate_user, item=rate_item)
    #         if rate_queryset.exists():
    #             return rate_queryset.first()
    def resolve_rate(self, info, user_id, item_id):
        item_queryset = Item.objects.all().filter(pk=item_id)
        if item_queryset.exists():
            rate_item = item_queryset.first()
        user_queryset = User.objects.all().filter(pk=user_id)
        if user_queryset.exists():
            rate_user = user_queryset.first()
        if rate_item is not None and rate_user is not None:
            rate_queryset = Rate.objects.all().filter(user=rate_user, item=rate_item)
            if rate_queryset.exists():
                return rate_queryset.first()
    #users
    # def resolve_user(self, info, email):
    #     print("user_query: " + email)
    #     user_queryset = User.objects.all().filter(email=email)
    #     if user_queryset.exists():
    #         return user_queryset.first()


    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

    def resolve_recommendations(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        item_ids = recommend_for_user(user.id)
        # print(item_ids)
        items = Item.objects.all().filter(pk__in=item_ids)
        return items




class SignupMutation(graphene.Mutation):
    # user = graphene.Field(UserType)
    token = graphene.String()

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

        token = get_token(user)
        # refresh_token = create_refresh_token(user)
        return SignupMutation(token=token)


class Mutation(graphene.ObjectType):
    signup = SignupMutation.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
