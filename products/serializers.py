from rest_framework import serializers
from .models import Product, Category
from accounts.models import Seller


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'company_name', 'is_verified']


class SellerDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'company_name', 'is_verified', 'products']

    def get_products(self, obj):
        request = self.context.get('request')
        products = obj.product_set.all()

        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size', 10)
        page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data).data



class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['seller']