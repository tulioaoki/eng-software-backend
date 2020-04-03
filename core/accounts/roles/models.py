from django.db import models


class Role(models.Model):
    ROLE_CHOICES = (
        ('0', 'Admin'),
        ('1', 'default')
    )

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        permissions = (
                        ("leitor", "Pode visualizar {}".format(verbose_name_plural)),
                        ("editor", "Pode visualizar e editar {}".format(verbose_name_plural)),
                       )
        default_permissions = ()

    def __unicode__(self):
        return self.role

    role = models.CharField(primary_key=True, choices=ROLE_CHOICES, max_length=1, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        return super(Role, self).save(*args, **kwargs)

    def getRole(self):
        return self.role