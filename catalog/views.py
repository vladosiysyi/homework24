from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views import View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Category
from .models import Product
from .forms import ProductForm
from .services import get_products_by_category
from django.core.cache import cache

class ProductsByCategoryView(TemplateView):
    template_name = 'catalog/products_by_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        products = get_products_by_category(category_id)
        context['category'] = category
        context['products'] = products
        return context

# Главная страница с товарами
class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Пробуем получить продукты из кеша
        products = cache.get('all_products')

        if products is None:
            # Если в кеше нет — получаем из БД и сохраняем в кеш
            products = Product.objects.filter(status='published')
            cache.set('all_products', products, 60 * 5)  # Кеш на 5 минут

        return products


# Страница "Контакты"
class ContactsView(TemplateView):
    template_name = 'contacts.html'


# Страница одного товара
@method_decorator(cache_page(60 * 15), name='dispatch')
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
