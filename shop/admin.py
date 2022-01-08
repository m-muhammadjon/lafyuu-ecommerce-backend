from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(Review)


class ProductColorItemInline(admin.TabularInline):
    model = ProductColor
    raw_id_fields = ['product']


class ProductImagesItemInline(admin.TabularInline):
    model = ProductImage
    raw_id_fields = ['product']


class ProductSizeItemInline(admin.TabularInline):
    model = ProductSize
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    list_filter = ['category', ]
    search_fields = ['name', ]
    inlines = [ProductColorItemInline, ProductImagesItemInline, ProductSizeItemInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag']
