from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import Basket, BasketItem
from .serializers import BasketItemSerializer, BasketSerializer


class BasketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        basket, created = Basket.objects.get_or_create(customer=request.user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data)


class BasketItemListCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        basket = get_object_or_404(Basket, customer=request.user)
        items = basket.basketitem_set.all()
        serializer = BasketItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        basket, created = Basket.objects.get_or_create(customer=request.user)
        request.data['basket'] = basket.id

        serializer = BasketItemSerializer(data=request.data)
        if serializer.is_valid():
            # Check if item already exists in basket
            product_id = request.data.get('product')
            existing_item = basket.basketitem_set.filter(product_id=product_id).first()

            if existing_item:
                # Update quantity if item exists
                existing_item.quantity += int(request.data.get('quantity', 1))
                existing_item.save()
                serializer = BasketItemSerializer(existing_item)
            else:
                # Create new item
                serializer.save(basket=basket)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasketItemDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        basket = get_object_or_404(Basket, customer=request.user)
        item = get_object_or_404(BasketItem, pk=pk, basket=basket)
        serializer = BasketItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        basket = get_object_or_404(Basket, customer=request.user)
        item = get_object_or_404(BasketItem, pk=pk, basket=basket)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

