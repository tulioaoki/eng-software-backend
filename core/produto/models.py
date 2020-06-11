from django.contrib.auth.models import User
from django.db import models

from core.categoria.models import Category


class Product(models.Model):
    class Meta(object):
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        permissions = (
            ("{}_{}_visualizar".format("geral", verbose_name_plural.lower()),
             "Pode visualizar {}".format(verbose_name_plural)),
            (
                "{}_{}_editar".format("geral", verbose_name_plural.lower()),
                "Pode visualizar e editar {}".format(verbose_name_plural)),
        )

        default_permissions = ()

    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    number_product = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    offer_price = models.FloatField(default=None, null=True, blank=True)
    images = models.ManyToManyField('ProductImage')
    categories = models.ManyToManyField(to=Category, blank=True)
    offer = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    class Meta(object):
        verbose_name = 'Product Image'
        verbose_name_plural = 'Products Images'
        permissions = (
            ("{}_{}_visualizar".format("geral", verbose_name_plural.lower()),
             "Pode visualizar {}".format(verbose_name_plural)),
            (
                "{}_{}_editar".format("geral", verbose_name_plural.lower()),
                "Pode visualizar e editar {}".format(verbose_name_plural)),
        )

        default_permissions = ()

    def __str__(self):
        return self.image_url

    id = models.AutoField(primary_key=True)
    image_url = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)


