from rest_framework import serializers
from .models import Basket, BasketItem
from products.serializers import ProductSerializer


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = BasketItem
        fields = ['id', 'basket', 'product', 'quantity', 'total_price']
        read_only_fields = ['basket', 'total_price']


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(source='basketitem_set', many=True, read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'customer', 'items']
        read_only_fields = ['customer']

