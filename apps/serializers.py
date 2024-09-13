from apps.documents import ProductDocument
from apps.models import Category, Product, ProductImage, User
from django.core.cache import cache
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import EmailField, IntegerField, ModelSerializer, Serializer


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'type'

class ProductDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ProductDocument

        fields = (
            'id',
            'name',
            'description'
        )

class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = 'id', 'image'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ()

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['user'] = UserModelSerializer(instance.owner).data
        repr['images'] = ProductImageModelSerializer(instance.images, many=True, context=self.context).data
        return repr


class ProductDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ()

    def to_representation(self, instance: Product):
        repr = super().to_representation(instance)
        repr['category'] = CategoryModelSerializer(instance.category).data
        return repr


class SendCodeMailSerializer(Serializer):
    email = EmailField(
        max_length=255,
        help_text='olimcola@gmail.com'
    )

    def validate_email(self, value):
        if not value:
            raise ValidationError('Email is required')
        return value


class VerifyCodeSerializer(Serializer):
    email = EmailField(
        max_length=255,
        help_text='olimcola@gmail.com'
    )
    code = IntegerField(
        help_text='Enter the 4-digit code sent to your email'
    )

    def validate_email(self, value):
        if not value:
            raise ValidationError('Email is required')
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        cache_code = cache.get(email)
        if code != cache_code:
            raise ValidationError('The code is incorrect or has expired!')
        return attrs
