from django.test import TestCase
from paymobApp.api.models import Product
from django.contrib.auth.models import User, Group
class ProductTestCase(TestCase):
    def setUp(self):
        user = User.objects.get_or_create(username='admin')[0]
        Product.objects.create(name="p1", price=10, createdBy=user)
        Product.objects.create(name="p2", price=20, createdBy=user)

    def test_fetch_all_products(self):
        """List all products """
        products = Product.objects.all()
        self.assertEqual(len(products), 2)
    
    def test_motify_product(self):
        product = Product.objects.filter(id=1)
        product.update(price=30, currency="USD")
        updatedProduct = Product.objects.filter(id=1).first()
        self.assertEqual(updatedProduct.price, 30)
