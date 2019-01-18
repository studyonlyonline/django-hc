from django.contrib import admin
from .models import Schemes, Category, Products, Variants

#creating inlines for admin

class ProductsInline(admin.StackedInline):
    model = Products

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductsInline
    ]

admin.site.register(Schemes)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Variants)

