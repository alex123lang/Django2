from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from .models import Product, BlogPost


# Create your views here.


class ProductListView(ListView):
    model = Product


class ProductContactView(TemplateView):
    model = Product
    template_name = 'catalog/contact.html'


class ProductDetailView(DetailView):
    model = Product


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
