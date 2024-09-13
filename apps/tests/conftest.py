import pytest
from apps.tests.factories import CategoryFactory, ProductFactory, ProductImageFactory, UserFactory


@pytest.fixture()
def user():
    return UserFactory.create_batch(10)


@pytest.fixture()
def category():
    return CategoryFactory.create_batch(10)


@pytest.fixture()
def product(user, category):
    return ProductFactory.create_batch(10)
