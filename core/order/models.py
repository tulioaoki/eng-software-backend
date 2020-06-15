from django.contrib.auth.models import User
from django.db import models
from core.purchases.models import ItemProduct
from ecommerce import settings


class Order(models.Model):
    class Meta(object):
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='Cliente',  null=False, blank=False, on_delete=models.DO_NOTHING)
    purchases = models.ManyToManyField(ItemProduct)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_value(self):
        valor = 0
        for p in self.purchases.all():
            valor = (p.product_price * p.quantity) + valor
        return valor

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

