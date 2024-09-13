from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    IntegerField,
    Model,
    TextChoices,
    TextField,
)
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        MANAGER = 'manager', 'Manager'
        MODERATOR = 'moderator', 'Moderator'


    balance = IntegerField(db_default=0)
    type = CharField(max_length=25, choices=Type.choices, db_default=Type.USER)


class Category(MPTTModel):
    name = CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')

class Product(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    is_premium = BooleanField(db_default=0)
    description = TextField(null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name="products")
    owner = ForeignKey('apps.User', CASCADE, related_name="products")
    created_at = DateTimeField(auto_now_add=True)

class ProductImage(Model):
    image = ImageField(upload_to='products/')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')

class ProductHistory(Model):
    name = CharField(max_length=255)
    price = IntegerField()
    deleted_at = DateTimeField(auto_now=True)

