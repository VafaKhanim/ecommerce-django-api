from django.urls import path
from .views import ProductListCreateView, ProductDetailView, ProductSearchView, CategoryListCreateView, CategoryDetailView, SellerListView, SellerDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name = 'products'),
    path('<slug:slug>/', ProductDetailView.as_view(), name = 'product_detail'),
    path('search/', ProductSearchView.as_view(), name='product-filter'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('sellers/', SellerListView.as_view(), name = 'seller-list'),
    path('sellers/<int:pk>/', SellerDetailView.as_view(), name='seller-detail')
]