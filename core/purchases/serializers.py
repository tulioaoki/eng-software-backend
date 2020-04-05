from rest_framework import serializers
from core.produto.serializers import ProductSerializer
from core.purchases.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Purchase
        
        fields = ["id","product","purchase","product_price","total_proce","created_at","updated_at",]

    def create(self, validated_data):
        product = validated_data.get('product')
        purchase = Purchase.objects.create(
            product=product,
            quantity=validated_data.get('quantity'),
        )
        return purchase
