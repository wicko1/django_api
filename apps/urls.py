from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from apps.schemas import schema
from apps.views import (
    CategoryListCreateAPIView,
    ProductListCreateAPIView,
    SendCodeAPIView,
    VerifyCodeAPIView,
)
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register("products", ProductDocumentViewSet, "products")

urlpatterns = [
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

    path('send-email', SendCodeAPIView.as_view(), name='send_email'),
    path('verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('category', CategoryListCreateAPIView.as_view(), name='category_list'),
    path('product-postgres', ProductListCreateAPIView.as_view(), name='product_list'),
]
