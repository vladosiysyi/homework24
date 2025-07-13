from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Category, Product

User = get_user_model()

admin.site.register(User)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'status')
    list_filter = ('category', 'status')
    search_fields = ('name', 'description')
    list_editable = ('status',)