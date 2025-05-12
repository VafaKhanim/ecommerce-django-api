from rest_framework import serializers
from .models import Product, Category
from accounts.models import Seller
from .paginations import CustomPagination


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
    total_products = serializers.IntegerField(
        source='products.count',
        read_only=True
    )

    class Meta:
        model = Seller
        fields = [
            'id',
            'company_name',
            'is_verified',
            'phone_number',
            'total_products',
            'products'
        ]

    def get_products(self, obj):
        request = self.context.get('request')
        products = obj.products.all()

        # Return unpaginated if no request or page parameter
        if not request or 'page' not in request.query_params:
            return ProductSerializer(products, many=True).data

        # Handle pagination
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data).data



class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['seller']