from apps.models import Product, ProductHistory, User
from apps.tests.conftest import product
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=Product)
def product_history(sender, instance: Product, **kwargs):
    ProductHistory.objects.create(product_id=instance.id, name=instance.name)

