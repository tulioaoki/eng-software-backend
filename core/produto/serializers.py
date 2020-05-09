from rest_framework import serializers
from core.categoria.models import Category
from core.categoria.serializers import CategorySerializer
from core.produto.models import Product, ProductImage, Offer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image_url", "created_at", "updated_at", ]

    def create(self, validated_data):
        product_image = ProductImage.objects.create(
            image_url=validated_data.get('image_url'),
        )
        return product_image

    def update(self, instance, validated_data):
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    images = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        
        fields = ["id", "images","name", "description","quantity","price","categories","created_at","updated_at",]

    def create(self, validated_data):
        categories_data = validated_data.get('categories')
        images = validated_data.get('images')
        product = Product.objects.create(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            quantity=validated_data.get('quantity'),
            price=validated_data.get('price')
        )
        if product and categories_data:
            for c in categories_data:
                category = get_category(c)
                product.categories.add(category)
        if product and images is not None:
            for i in images:
                img = ProductImageSerializer.create(ProductImageSerializer(), validated_data=i)
                product.images.add(img)
        product.save()
        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.get('categories')
        if categories_data:
            for c in categories_data:
                category = get_category(c.get('id'))
                instance.categories.add(category)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.name = validated_data.get('name', instance.name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class OfferSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ["id","new_price", "product", "created_at","updated_at", ]

    def create(self, validated_data):
        id = validated_data.get('product')
        p = Product.objects.get(pk=id)
        offer = Offer.objects.create(
            product=p,
            new_price=validated_data.get('new_price')
        )
        return offer

    def update(self, instance, validated_data):
        instance.new_price = validated_data.get('new_price', instance.price)
        instance.save()
        return instance


def get_category(category):
    try:
        return Category.objects.get(pk=category)
    except Category.DoesNotExist:
        return None
