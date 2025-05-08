from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q

from accounts.permissions import IsSuperUserOrReadOnly, IsVerifiedSeller, IsVerifiedSellerOrReadOnly
from .models import Product, Category
from accounts.models import Seller
from .serializers import ProductSerializer, CategorySerializer, SellerSerializer




class ProductListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Check if user has seller profile and is verified
        if not hasattr(request.user, 'seller_profile') or not request.user.seller_profile.is_verified:
            return Response(
                {"error": "Only verified sellers can add products"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(seller=request.user.seller_profile)  # Use seller_profile instead of user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [IsVerifiedSellerOrReadOnly]  # Changed permission

    def get_object(self, slug):
        return get_object_or_404(
            Product.objects.select_related('seller', 'category'),
            slug=slug
        )

    def get(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, slug):
        product = self.get_object(slug)

        # Ownership check is now handled by IsVerifiedSellerOrReadOnly
        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        product = self.get_object(slug)
        # Ownership check handled by permission class
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('search', '')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        category = request.query_params.get('category')
        seller = request.query_params.get('seller')

        filters = Q(name__icontains=query) | Q(description__icontains=query)

        # Price filtering
        if min_price:
            try:
                filters &= Q(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                filters &= Q(price__lte=float(max_price))
            except ValueError:
                pass

        # Category filtering
        if category:
            filters &= Q(category__slug=category)

        # Seller filtering
        if seller:
            if seller.isdigit():
                filters &= Q(seller__id=int(seller))
            else:
                filters &= Q(seller__company_name__icontains=seller) | Q(seller__user__username__icontains=seller)

        products = Product.objects.filter(filters)
        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class CategoryListCreateView(APIView):
    permission_classes = [IsSuperUserOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsSuperUserOrReadOnly]

    def get_object(self, slug):
        return get_object_or_404(Category, slug=slug)

    def get(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, slug):
        category = self.get_object(slug)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        category = self.get_object(slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class SellerListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sellers = Seller.objects.all()
        serializer = SellerSerializer(categories, many=True)
        return Response(serializer.data)






