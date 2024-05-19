from django.urls import path
from catalog.apps import CatalogConfig

from catalog.views import ProductListView, ProductDetailView, ProductContactView, BlogPostListView, BlogPostDetailView, \
    BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView


app_name = CatalogConfig.name

urlpatterns = [
    path('contact/', ProductContactView.as_view(), name='contact'),
    path('', ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('blog/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blog/create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blog/<int:pk>/update/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]
