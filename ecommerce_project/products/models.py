from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product_Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity_in_stock = models.IntegerField()
    category = models.ForeignKey(Product_Category,on_delete=models.SET_NULL,related_name="products", null=True, blank=True)
    updated_by = models.ForeignKey(User,on_delete=models.PROTECT,related_name="products")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["-updated_at"]),
        ]

    def __str__(self):
        return self.name