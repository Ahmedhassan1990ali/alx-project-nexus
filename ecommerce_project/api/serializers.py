from rest_framework import serializers
from products.models import Product, Product_Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = Product
        exclude = ["updated_by"]

class ProductCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Product_Category
        fields = "__all__"