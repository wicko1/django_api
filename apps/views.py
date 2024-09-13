from random import randint

from apps.documents import ProductDocument
from apps.filters import ProductFilter
from apps.models import Category, Product
from apps.paginations import ProductPagination
from apps.serializers import (
    CategoryModelSerializer,
    ProductDocumentSerializer,
    ProductListModelSerializer,
    SendCodeMailSerializer,
    VerifyCodeSerializer,
)
from django.core.cache import cache
from django.core.mail import send_mail
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, SuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response


class ProductDocumentViewSet(DocumentViewSet):
    document = ProductDocument
    serializer_class = ProductDocumentSerializer

    filter_backends = [
        SearchFilterBackend,
        SuggesterFilterBackend
    ]
    search_fields = ('name', 'description')


@extend_schema(tags=['category'])
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


@extend_schema(tags=['product'])
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListModelSerializer
    filterset_class = ProductFilter
    pagination_class = ProductPagination


@extend_schema(tags=['auth'])
class SendCodeAPIView(GenericAPIView):
    serializer_class = SendCodeMailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = randint(1000, 9999)
        cache.set(email, code, timeout=120)
        print(f"Email: {email}, Code: {code}")
        send_mail(
            'Your Verification Code',
            f'Your verification code is {code}',
            'asadbekmehmonjonov5@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Code sent successfully"}, status=status.HTTP_200_OK)


@extend_schema(tags=['auth'])
class VerifyCodeAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "OK"}, status=status.HTTP_200_OK)
