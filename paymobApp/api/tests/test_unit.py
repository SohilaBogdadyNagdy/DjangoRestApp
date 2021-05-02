from django.test import TestCase
from paymobApp.api.models import Product
from django.contrib.auth.models import User, Group
class ProductTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='admin', password='admin')
        Product.objects.create(name="p1", price=10, createdBy=user)
        Product.objects.create(name="p2", price=20, createdBy=user)

    def test_fetch_all_products(self):
        """List all products """
        products = Product.objects.all()
        self.assertEqual(len(products), 2)
    
    def test_motify_product(self):
        product = Product.objects.filter(id=1)
        product.update(price=30)
        self.assertEqual(Product.objects.filter(id=1).price, 30)
