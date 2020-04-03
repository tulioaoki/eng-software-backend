# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Role



class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'