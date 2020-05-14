# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin, _user_has_perm, _user_has_module_perms)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from core.accounts.roles.models import Role
from core.produto.models import Product
from core.purchases.models import ItemProduct
from core.validators import only_numbers, only_char, positive, validate_email


class MyUserManager(BaseUserManager):
    def create_user(self,username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )

        user.is_active=True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            username=username,
            password=password,
            )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomUser(AbstractBaseUser,PermissionsMixin):

    class Meta:
        verbose_name = u'usuario'
        verbose_name_plural =u'usuarios'
        default_permissions = ()

    username = models.CharField(
        validators=[validate_email],
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    name = models.CharField('Nome', max_length=50, validators=[only_char])

    ddd_phone_comercial = models.CharField(max_length=2, validators=[only_numbers], blank=True, null=True)
    comercial_phone = models.CharField('Telefone', max_length=9, validators=[only_numbers, positive], blank=True, null=True)
    ddd_phone = models.CharField(max_length=2, validators=[only_numbers], blank=True, null=True)
    phone = models.CharField('Telefone', max_length=15, validators=[only_numbers, positive], blank=True, null=True)
    email_alternativo = models.EmailField('email alterinativo', unique=False, blank=True, null=True)

    tratamento = models.CharField(max_length=30, blank=True, null=True)
    tipo_logradouro = models.CharField(max_length=60, blank=True, null=True)
    logradouro = models.CharField(max_length=80, blank=True, null=True)
    numero_logradouro = models.IntegerField(blank=True, null=True)
    complemento = models.CharField(max_length=80, blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    localidade = models.CharField(max_length=80, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=8,validators=[only_numbers], blank=True, null=True)
    notas = models.CharField(max_length=100, blank=True, null=True)

    favorites = models.ManyToManyField(Product, related_name="favoritos", null=True)
    cart = models.ManyToManyField(ItemProduct, related_name="carrinho", null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def clean(self):
        self.name = self.name.capitalize()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        # __unicode__ on Python 2
        return self.name


    def has_perm(self, perm, obj=None,**kwargs):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None, **kwargs):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        return all(self.has_perm(perm, obj, kwargs=kwargs) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser or self.is_admin:
            return True
        return _user_has_module_perms(self, app_label)

    def update_role(self, role):
        self.role = role

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        super(AbstractBaseUser, self).save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None









