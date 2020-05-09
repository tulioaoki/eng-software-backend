from django.db import models


class Image(models.Model):
    class Meta(object):
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        permissions = (
            ("{}_{}_visualizar".format("geral", verbose_name_plural.lower()),
             "Pode visualizar {}".format(verbose_name_plural)),
            (
                "{}_{}_editar".format("geral", verbose_name_plural.lower()),
                "Pode visualizar e editar {}".format(verbose_name_plural)),
        )

        default_permissions = ()

    def __str__(self):
        return self.url

    id = models.AutoField(primary_key=True)
    url = models.TextField(null=True, blank=True)
    base_64 = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)


class Carrosel(models.Model):
    class Meta(object):
        verbose_name = 'Carrosel'
        verbose_name_plural = 'Carrosel'
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
    images = models.ManyToManyField(Image)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Carrosel, self).save(*args, **kwargs)
