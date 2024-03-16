from rest_framework import serializers
from .models import Product, Supplier


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'product_supplier',
            'product_category',
            'quantity',
            'price',
            'image'
        ]


class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.ReadOnlyField(source='product_supplier.name')
    category = serializers.ReadOnlyField(source='product_category.name')

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'supplier',
            'category',
            'quantity',
            'price',
            'image'
        ]
        

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
