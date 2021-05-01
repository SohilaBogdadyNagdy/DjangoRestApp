from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    isPaid = models.BooleanField(default=False, blank=True, null=True)
    price = models.IntegerField()
    currency = models.CharField(max_length=3)
    createdBy = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)
    purchasedBy = models.ForeignKey('auth.User', related_name='purchases', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name