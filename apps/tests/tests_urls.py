import pytest
from rest_framework.reverse import reverse_lazy


class TestUrl:
    def test_product(self):
        url = reverse_lazy('product_list')
        assert url == '/api/v1/product'

    def test_category(self):
        url = reverse_lazy('category_list')
        assert url == '/api/v1/category'

    def test_auth(self):
        url = reverse_lazy('send_email')
        assert url == '/api/v1/send-email'
        url = reverse_lazy('verify_code')
        assert url == '/api/v1/verify-code'