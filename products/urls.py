from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductSearchView,
    CategoryListCreateView,
    CategoryDetailView,
    SellerListView,
    SellerDetailView
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='products'),
    path('search/', ProductSearchView.as_view(), name='product-filter'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    # Seller paths should come before the slug pattern
    path('sellers/', SellerListView.as_view(), name='seller-list'),
    path('sellers/<int:pk>/', SellerDetailView.as_view(), name='seller-detail'),

    # Product detail slug pattern should be LAST
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]