from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Генерирует тестовые продукты'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        electronics = Category.objects.create(name='Электроника', description='...')
        clothing = Category.objects.create(name='Одежда', description='...')

        Product.objects.create(name='Наушники', description='...', category=electronics, price=1999)
        Product.objects.create(name='Куртка', description='...', category=clothing, price=4999)

        self.stdout.write(self.style.SUCCESS('Данные успешно созданы'))
