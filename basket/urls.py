from django.urls import path
from .views import BasketItemListCreate, BasketItemDetail, BasketView

urlpatterns = [
    path('', BasketView.as_view(), name='basket-detail'),
    path('items/', BasketItemListCreate.as_view(), name = 'basketitem-list-create'),
    path('items/<int:pk>/', BasketItemDetail.as_view(), name = 'basketitem-detail')
]