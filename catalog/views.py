from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from .models import Product
from .forms import ProductForm


# Главная страница с товарами
class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'


# Страница "Контакты"
class ContactsView(TemplateView):
    template_name = 'contacts.html'


# Страница одного товара
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


# CRUD: список товаров
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


# CRUD: создание товара
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')


# CRUD: обновление товара
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')


# CRUD: удаление товара
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
