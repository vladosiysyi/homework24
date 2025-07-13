from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views import View

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
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Список названий групп пользователя для удобной проверки в шаблоне
        context['user_group_names'] = self.request.user.groups.values_list('name', flat=True)
        return context


# CRUD: создание товара
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# CRUD: обновление товара
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner


# CRUD: удаление товара
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.groups.filter(name="Модератор продуктов").exists()


# Отмена публикации товара (для пользователей с правом can_unpublish_product)
class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.user.has_perm('catalog.can_unpublish_product'):
            product.status = 'draft'
            product.save()
            return redirect('product_list')
        return HttpResponseForbidden("У вас нет прав для отмены публикации.")
