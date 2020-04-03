from rest_framework import serializers

from core.categoria.models import Category
from core.categoria.serializers import CategorySerializer
from core.produto.models import Product


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Product
        
        fields = ["id", "number_product", "name", "description","quantity","price","categories","created_at","updated_at",]

    def create(self, validated_data):
        categories_data = validated_data.get('categories')
        product = Product.objects.create(
            number_product=validated_data.get('number_product'),
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            quantity=validated_data.get('quantity'),
            price=validated_data.get('price')
        )
        if product and categories_data:
            for c in categories_data:
                category = get_category(c)
                product.categories.add(category)
        product.save()
        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.get('categories')
        if categories_data:
            for c in categories_data:
                category = get_category(c.get('id'))
                instance.categories.add(category)
        instance.number_product = validated_data.get('number_product', instance.number_product)
        instance.name = validated_data.get('name', instance.name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
    
def get_category(category):
    try:
        return Category.objects.get(pk=category)
    except Category.DoesNotExist:
        return None
