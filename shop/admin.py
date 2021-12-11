from django.contrib import admin

from .models import MainCategory, Category, Product


admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Product)
