from django import forms
from .models import Product
from django.core.exceptions import ValidationError

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


        self.fields['name'].widget.attrs.update({'placeholder': 'Введите название продукта'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Введите описание продукта', 'rows': 4})
        self.fields['price'].widget.attrs.update({'min': '0', 'step': '0.01'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if any(word in name.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Название содержит запрещённые слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if any(word in description.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Описание содержит запрещённые слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price
