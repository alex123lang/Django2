from django import forms
from django.forms import ModelForm, BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'photo',
            'category',
            'price',
        ]

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        forbidden_words = ['казино',
                           'криптовалюта',
                           'крипта',
                           'биржа',
                           'дешево',
                           'бесплатно',
                           'обман',
                           'полиция',
                           'радар']

        for forbidden_word in forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise forms.ValidationError('Присутствует запрещенное слово')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        forbidden_words = ['казино',
                           'криптовалюта',
                           'крипта',
                           'биржа',
                           'дешево',
                           'бесплатно',
                           'обман',
                           'полиция',
                           'радар']

        for forbidden_word in forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise forms.ValidationError('Присутствует запрещенное слово')

        return cleaned_data

class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ('is_published', 'description', 'category')

class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
