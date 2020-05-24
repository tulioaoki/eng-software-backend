from django.db import models
from django.db.models import DO_NOTHING

from core.produto.models import Product


class ItemProduct(models.Model):
    class Meta(object):
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        permissions = (
            ("{}_{}_visualizar".format("geral", verbose_name_plural.lower()),
             "Pode visualizar {}".format(verbose_name_plural)),
            (
                "{}_{}_editar".format("geral", verbose_name_plural.lower()),
                "Pode visualizar e editar {}".format(verbose_name_plural)),
        )

        default_permissions = ()

    def __str__(self):
        return self.id

    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=DO_NOTHING)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    product_price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.product.offer:
            self.product_price = self.product.offer_price
        else:
            self.product_price = self.product.price
        self.total_price = self.product_price * self.quantity
        super(ItemProduct, self).save(*args, **kwargs)
