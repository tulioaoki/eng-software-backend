from rest_framework import serializers
from core.categoria.models import Category
from core.categoria.serializers import CategorySerializer
from core.produto.models import Product, ProductImage


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
        
        fields = ["id", "images", "offer", "offer_price", "name", "description","peso","unidade","marca" ,"quantity", "price", "categories", "created_at", "updated_at",]

    def create(self, validated_data):
        categories_data = validated_data.get('categories')
        images = validated_data.get('images')
        product = Product.objects.create(
            name=validated_data.get('name'),
            peso=validated_data.get('peso'),
            unidade=validated_data.get('unidade'),
            marca=validated_data.get('marca'),
            description=validated_data.get('description'),
            quantity=validated_data.get('quantity'),
            price=validated_data.get('price'),
            offer=validated_data.get('offer'),
            offer_price=validated_data.get('offer_price')
        )
        if product and categories_data:
            for c in categories_data:
                category = get_category(c)
                if category is not None:
                    product.categories.add(category)
        if product and images is not None:
            for i in images:
                img = ProductImageSerializer.create(ProductImageSerializer(), validated_data=i)
                product.images.add(img)
        product.save()
        return product



def get_category(category):
    try:
        return Category.objects.get(pk=category)
    except Category.DoesNotExist:
        return None


def get_image(image_id):
    try:
        return Category.objects.get(pk=image_id)
    except Category.DoesNotExist:
        return None


class ProductEditSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),many=True, read_only=False,)
    images = ProductImageSerializer(read_only=False, many=True)

    class Meta:
        model = Product

        fields = ["id", "images","offer","offer_price", "name", "description", "peso","unidade","marca"
                  "quantity", "price", "categories", "created_at", "updated_at", ]

    def update(self, instance, validated_data):
        categories_data = validated_data.get('categories')
        images = validated_data.get('images')
        if categories_data:
            request_categories = []
            for c in categories_data:
                request_categories.append(c)
                if c in instance.categories.all():
                    pass
                else:
                    instance.categories.add(c)
            for k in instance.categories.all():
                if k not in request_categories:
                    instance.categories.remove(k)

        if images:
            request_images = []
            for i in images:
                id = i.get('id')
                if id is None:
                    image = ProductImageSerializer.create(ProductImageSerializer(), validated_data=i)
                else:
                    image = get_image(id)
                request_images.append(image)
                if image in instance.categories.all():
                    pass
                else:
                    instance.images.add(image)
            for k in instance.images.all():
                if k not in request_images:
                    instance.images.remove(k)

        instance.name = validated_data.get('name', instance.name)
        instance.offer = validated_data.get('offer', instance.offer)
        instance.offer_price = validated_data.get('offer_price', instance.offer_price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        if instance.offer_price and instance.price and instance.offer_price > instance.price:
            instance.offer_price = instance.price
        instance.description = validated_data.get('description', instance.description)
        instance.peso = validated_data.get('peso', instance.peso)
        instance.unidade = validated_data.get('unidade', instance.unidade)
        instance.marca = validated_data.get('marca', instance.marca)
        instance.save()
        return instance
