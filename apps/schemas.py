import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from apps.models import Product, Category, User


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, name):
        category = Category.objects.create(
            name=name
        )
        return CreateCategory(category=category)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Int(required=True)
        description = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        owner_id = graphene.Int(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, description, category_id, owner_id):
        owner = User.objects.get(id=owner_id)
        category = Category.objects.get(id=category_id)
        product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            category=category,
            owner=owner,
        )
        return CreateProduct(product=product)


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return CreateUser(user=user)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name):
        try:
            category = Category.objects.get(id=id)
            category.name = name
            category.save()
            return UpdateCategory(category=category)
        except Category.DoesNotExist:
            raise GraphQLError("Category not found.")


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, id, username=None, email=None, password=None):
        try:
            user = User.objects.get(id=id)
            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if password is not None:
                user.set_password(password)
            user.save()
            return UpdateUser(user=user)
        except User.DoesNotExist:
            raise GraphQLError("User not found.")


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        price = graphene.Int()
        description = graphene.String()
        category_id = graphene.Int()
        owner_id = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, id, name=None, price=None, description=None, category_id=None, owner_id=None):
        try:
            product = Product.objects.get(id=id)
            if name is not None:
                product.name = name
            if price is not None:
                product.price = price
            if description is not None:
                product.description = description
            if category_id is not None:
                product.category = Category.objects.get(id=category_id)
            if owner_id is not None:
                product.owner = User.objects.get(id=owner_id)
            product.save()
            return UpdateProduct(product=product)
        except Product.DoesNotExist:
            raise GraphQLError("Product not found.")
        except Category.DoesNotExist:
            raise GraphQLError("Category not found.")
        except User.DoesNotExist:
            raise GraphQLError("User not found.")



class Query(graphene.ObjectType):
    users1 = graphene.List(UserType, description="Userlar")
    products = graphene.List(ProductType, description="Productlar ")
    categories = graphene.List(CategoryType, description='Bu kategoriya hisoblanadi')

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_users(self, info, **kwargs):
        return User.objects.none()

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_product = CreateProduct.Field()
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
