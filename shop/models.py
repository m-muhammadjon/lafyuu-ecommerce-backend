import os
import uuid

from django.db import models


def get_file_path_product(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('product', filename)


class MainCategory(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Main categories'
        verbose_name_plural = 'Main categories'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=50)
    main_category = models.ForeignKey(MainCategory,
                                      on_delete=models.CASCADE,
                                      related_name='categories')

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'Category {self.title} for {self.main_category.title}'


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.ImageField(upload_to=get_file_path_product)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product,
                                related_name='reviews',
                                on_delete=models.CASCADE)

