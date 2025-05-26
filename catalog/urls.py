from django.urls import path
from .views import HomeView, ContactsView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
]
