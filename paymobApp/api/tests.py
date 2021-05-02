from django.urls import reverse
from rest_framework import status
from base64 import b64encode

from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User, Group
from .models import Product


class ProductTests(APITestCase):
    def setUp(self):
        adminUser = User(password='admin', username='admin')
        adminUser.save()
        userAndPass = b64encode(b"admin:admin").decode("ascii")
        self.headers = {'Authorization': 'Basic ' + userAndPass}
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + userAndPass)

    def test_create_product(self):
        """
        Ensure we can create a new product object.
        """
        url = reverse('product-list')
        data = {'name': 'new product', 'price': 90}
        response = self.client.post(url, data, headers= self.headers, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'new product')

    def test_List_products(self):
        """
        Ensure both admins and normal users can list products object.
        """
        url = reverse('product-list')
        response = self.client.get(url, headers= self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'new product')

    def test_get_product(self):
        """
        Ensure both admins and normal users can get one product object.
        """
        url = reverse('product-list')
        url += '1'
        response = self.client.get(url, headers= self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_product(self):
        """
        Ensure only admins can modify product object.
        """
        url = reverse('product-list')
        url += '1'
        response = self.client.put(url, { "price": 30000 } ,headers= self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pay_product(self):
        """
        Ensure only normal users can purchase product.
        """
        url = reverse('purchase')
        url += '1'
        response = self.client.patch(url,headers= self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
