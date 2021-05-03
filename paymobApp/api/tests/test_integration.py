from django.urls import reverse
from rest_framework import status
from base64 import b64encode

from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User, Group
from paymobApp.api.models import Product


class ProductTests(APITestCase):
    def setUp(self):
        adminGroup = Group.objects.get_or_create(name='admin')[0]
        normalGroup = Group.objects.get_or_create(name='normal')[0]
        adminUser = User.objects.get_or_create(username='admin')[0]
        adminUser.groups.add(adminGroup)
        adminUser.set_password('admin!@#$')
        adminUser.save()
        userAndPass = b64encode(b"admin:admin!@#$").decode("ascii")
        self.headers = {'Authorization': 'Basic ' + userAndPass}
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + userAndPass)

        normalUser = User.objects.get_or_create(username='normal')[0]
        normalUser.set_password('normal!@#$')
        normalUser.groups.add(normalGroup)
        normalUser.save()
        self.authorizationHeaderForNormalUser = {
            'Authorization': 'Basic ' + b64encode(b"normal:normal!@#$").decode("ascii")
        }
        Product.objects.create(name='test', price=200, currency='USD', createdBy=adminUser)

    def test_create_product(self):
        """
        Ensure we can create a new product object.
        """
        url = reverse('product-list')
        data = {'name': 'new product', 'price': 90, 'currency': 'USD'}
        response = self.client.post(url, data, headers= self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_List_products(self):
        """
        Ensure both admins and normal users can list products object.
        """
        url = reverse('product-list')
        response = self.client.get(url, headers= self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'test')

    def test_get_product(self):
        """
        Ensure both admins and normal users can get one product object.
        """
        url = reverse('product-list')
        url += '1'
        response = self.client.get(url, headers= self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_product(self):
        """
        Ensure only admins can modify product object.
        """
        url = reverse('product-list')
        url += '1'
        response = self.client.put(url, { "price": 30000 , "currency": "USD"} ,headers= self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

