from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .paginations import CustomPagination
from accounts.permissions import IsSuperUserOrReadOnly, IsVerifiedSellerOrReadOnly
from .models import Product, Category
from accounts.models import Seller
from .serializers import ProductSerializer, CategorySerializer, SellerSerializer, SellerDetailSerializer




class ProductListCreateView(APIView):
    permission_classes = [IsVerifiedSellerOrReadOnly]
    pagination_class = CustomPagination

    def get(self, request):
        products = Product.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(seller=request.user.seller_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductDetailView(APIView):
    permission_classes = [IsVerifiedSellerOrReadOnly]

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
        self.check_object_permissions(request, product)
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
        # Ownership check handled by IsVerifiedSellerOrReadOnly
        self.check_object_permissions(request, product)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductSearchView(APIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

    def get(self, request):
        search_query = request.query_params.get('search', '').strip()
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        category = request.query_params.get('category')
        seller = request.query_params.get('seller')


        filters = Q()
        if search_query:
            filters &= (
                    Q(name__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(slug__icontains=search_query)
            )

        try:
            if min_price:
                filters &= Q(price__gte=float(min_price))
            if max_price:
                filters &= Q(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass


        if category:
            filters &= (
                    Q(category__slug__icontains=category) |
                    Q(category__name__icontains=category)
            )


        if seller:
            if seller.isdigit():
                filters &= Q(seller__id=int(seller))
            else:
                filters &= (Q(seller__company_name__icontains=seller) |
                            Q(seller__user__username__icontains=seller))


        products = Product.objects.filter(filters).distinct()
        print(f"Tapılan məhsul sayı: {products.count()}")


        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(products, request)


        serializer = ProductSerializer(
            result_page,
            many=True,
            context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)



class CategoryListCreateView(APIView):
    permission_classes = [IsSuperUserOrReadOnly]
    pagination_class = CustomPagination

    def get(self, request):
        categories = Category.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(categories, request)

        serializer = CategorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


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
        sellers = Seller.objects.all().order_by('id')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(sellers, request)

        serializer = SellerSerializer(
            result_page,
            many=True,
            context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)



class SellerDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        seller = get_object_or_404(
            Seller.objects.prefetch_related('products'),
            pk=pk
        )
        serializer = SellerDetailSerializer(
            seller,
            context={'request': request}
        )
        return Response(serializer.data)





