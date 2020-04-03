# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.accounts.roles.models import Role
from core.accounts.utils import validate_role
from .models import CustomUser



class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name', 'email_alternativo',    
                  'username', 'is_admin' 'phone', 'ddd_phone_comercial',
                  'comercial_phone', "ddd_phone","phone", 'tratamento', 'logradouro','tipo_logradouro',
                  'numero_logradouro',"complemento", "bairro","localidade","cidade","uf","cep","notas")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id','name','email_alternativo',
                  'username','is_admin','phone','password', 'ddd_phone_comercial',
                  'comercial_phone', "ddd_phone","phone", 'tratamento','logradouro','tipo_logradouro',
                  'numero_logradouro',"complemento", "bairro","localidade","cidade","uf","cep","notas")


    def create(self, validated_data,):

        user = CustomUser.objects.create(
            username=validated_data.get('username'),
            name=validated_data.get('name'),
            phone=validated_data.get('phone'),
            email_alternativo=validated_data.get('email_alternativo'),
            ddd_phone_comercial=validated_data.get("ddd_phone_comercial"),
            comercial_phone=validated_data.get("comercial_phone"),
            ddd_phone=validated_data.get("ddd_phone_comercial"),
            tratamento=validated_data.get("tratamento"),
            logradouro=validated_data.get("logradouro"),
            tipo_logradouro=validated_data.get("tipo_logradouro"),
            numero_logradouro=validated_data.get("numero_logradouro"),
            complemento=validated_data.get("complemento"),
            bairro=validated_data.get("bairro"),
            localidade=validated_data.get("localidade"),
            cidade=validated_data.get("cidade"),
            uf=validated_data.get("uf"),
            cep=validated_data.get("cep"),
            notas=validated_data.get("notas"),

        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email_alternativo = validated_data.get('email_alternativo', instance.email_alternativo)
        instance.role = validated_data.get( instance.role)
        instance.save()
        return instance


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','username','profile','name', 'phone', ]
