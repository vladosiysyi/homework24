# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Product

def home_view(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def contacts_view(request):
    return render(request, 'contacts.html')

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})