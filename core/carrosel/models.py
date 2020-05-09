from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    class Meta(object):
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
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
    name = models.CharField(max_length=20)
    # categoria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
