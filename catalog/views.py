# Create your views here.

from django.views.generic import TemplateView, ListView, DetailView
from .models import Product


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

class ContactsView(TemplateView):
    template_name = 'contacts.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'