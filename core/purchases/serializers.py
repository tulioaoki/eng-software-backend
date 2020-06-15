from rest_framework import serializers

from core.produto.models import Product
from core.produto.serializers import ProductSerializer
from core.purchases.models import ItemProduct


class ItemProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ItemProduct
        
        fields = ["id","product","quantity","product_price","total_price","created_at","updated_at",]

    def create(self, validated_data):
        product = validated_data.get('product')
        product = Product.objects.get(pk=product)
        item = ItemProduct.objects.create(
            product=product,
            quantity=validated_data.get('quantity'),
        )
        return item


class ItemProductSerializerPkOnly(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = ItemProduct

        fields = ["id", "product", 'quantity', "product_price", "total_price", "created_at", "updated_at", ]


