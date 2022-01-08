import os
import uuid
from math import floor

from django.db import models
from django.utils.safestring import mark_safe

from account.models import User


def get_file_path_product(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('product', filename)


class Category(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey("Category",
                               related_name="childs",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_benefit(self):
        if self.is_discount:
            return 100 - floor(self.discount_price / self.price * 100)
        return 0

    def get_total_star(self):
        return sum(item.star for item in self.reviews.all()) / len(self.reviews.all())


class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to=get_file_path_product)
    title = models.CharField(max_length=255)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 60px; height:60px; object-fit: contain;"/>' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    def __str__(self):
        return f'Image for product {self.product.name}.'


class ProductSize(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='sizes')
    size = models.DecimalField(max_digits=20, decimal_places=1)

    def __str__(self):
        return f'{self.size} size for product {self.product.name}.'


class ProductColor(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='colors')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} color for product {self.product.name}.'


# class Review(models.Model):
#     product = models.OneToOneField(Product,
#                                    related_name='reviews',
#                                    on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'Review for {self.product.name}'
#
#     def get_total_star(self):
#         return sum(item.star for item in self.items.all()) / len(self.items.all())


class Review(models.Model):
    user = models.ForeignKey(User,
                             related_name='reviews',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='reviews',
                                on_delete=models.CASCADE)
    star = models.DecimalField(decimal_places=1, max_digits=2)
    body = models.TextField()
    is_top = models.BooleanField(default=True)

    def __str__(self):
        return self.body[:100]
