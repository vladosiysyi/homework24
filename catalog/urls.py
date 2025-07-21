from django.urls import path
from .views import (
    HomeView, ContactsView, ProductDetailView,
    ProductListView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, ProductUnpublishView, ProductsByCategoryView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish')
]
