from apps.models import Category, Product, ProductImage, User
from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin


@register(ProductImage)
class ProductImageModelAdmin(ModelAdmin):
    pass


@register(Product)
class ProductModelAdmin(ModelAdmin):
    pass


@register(User)
class ProductModelAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'balance']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email",  "password1", "password2", "balance"),
            },
        ),
    )


@register(Category)
class CategoryModelAdmin(ModelAdmin):
    pass
