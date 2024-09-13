import pytest
from apps.models import Category, Product
from rest_framework import status
from rest_framework.reverse import reverse_lazy


@pytest.mark.django_db
class TestViews:
    def test_product_list_has_image_with_filter(self, client, product):
        query = {
            'has_image': True
        }
        url = reverse_lazy('product_list')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert product['images']

    def test_product_list_with_filter(self, client, product):
        query = {
            'owner_type': 'admin'
        }
        url = reverse_lazy('product_list')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert product['user']['type'] == 'admin'

    def test_product_list_is_premium(self, client, product):
        query = {
            'is_premium': True
        }
        url = reverse_lazy('product_list')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for i in response['results']:
            assert i['is_premium']

        query = {
            'is_premium': False
        }
        url = reverse_lazy('product_list')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for i in response['results']:
            assert not i['is_premium']

    def test_product_from_price_to_price(self, client, product):
        query = {
            "from_price": 10000,
            "to_price": 15000,
        }
        url = reverse_lazy('product_list')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert query['from_price'] <= product['price'] <= query['to_price']

    def test_product_with_search(self, client, product):
        key = 'ProDuCt'
        query = {
            'search': key,
        }
        url = reverse_lazy('product_list')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            if key.lower() in product['name'].lower():
                assert key.lower() in product['name'].lower()
            else:
                product = Product.objects.get(id=product['id'])
                assert key.lower() in product['description'].lower()

    def test_product_list_with_category_filter(self, client, product, category):
        query = {
            "category": category.id
        }
        url = reverse_lazy('product_list')
        response = client.get(url, query)
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        for product in response['results']:
            assert product['category'] == category.id