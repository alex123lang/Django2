from django import forms
from django.forms import ModelForm

from .models import Product, Version


class ProductForm(ModelForm):
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


class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
