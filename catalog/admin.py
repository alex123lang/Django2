from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', )
    list_filter = ('price',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)

