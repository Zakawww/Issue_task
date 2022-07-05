from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'count', 'price']
    list_filter = ['category']
    search_fields = ['name', 'category']
    fields = ['name', 'description', 'category', 'count', 'price']
    list_display_links = ['id', 'name', 'category']


admin.site.register(Product, ProductAdmin)