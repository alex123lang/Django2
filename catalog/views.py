from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, BlogPost, Version
from catalog.service import get_product_from_cache


# Create your views here.


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Главная страница'
    }
    paginate_by = 4

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        return get_product_from_cache()


class ProductContactView(TemplateView):
    model = Product
    template_name = 'catalog/contact.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    extra_context = {
        'title': 'О продукте'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        versions = Version.objects.filter(product=product, is_active=True)

        # You can decide how to handle multiple versions here
        # For example, you might want to select the first one:
        version = versions.first() if versions.exists() else None

        context['version'] = version
        return context

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if self.request.user == product.author:
            product.save()
            return product
        raise PermissionDenied


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        context_data['formset'] = VersionFormset()
        return context_data

    """def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)"""

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.author or user.is_superuser:
            return ProductForm
        elif user.has_perm('catalog.unpublish_a_product') and user.has_perm(
                'catalog.change_description_product') and user.has_perm('catalog.change_category_product'):
            return ProductModeratorForm
        else:
            raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class BlogPostListView(ListView):
    model = BlogPost

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'published']
    success_url = reverse_lazy('catalog:blogpost_list')

    def form_valid(self, form):
        if form.is_valid():
            new_name = form.save()
            new_name.slug = slugify(new_name.title)
            new_name.save()

        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'published']

    def get_success_url(self):
        return reverse('catalog:blogpost_detail', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('catalog:blogpost_list')
