from rest_framework import serializers

from core.order.models import Order
from core.purchases.serializers import ItemProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    purchases = ItemProductSerializer(read_only=False,many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data, user=None):
        items = validated_data.get('purchases')
        order = Order.objects.create(
            owner=user,
        )

        if order and items is not None:
            for i in items:
                item = ItemProductSerializer.create(ItemProductSerializer(), validated_data=i)
                p = item.product
                p.times_bought = p.times_bought + item.quantity
                order.purchases.add(item)
                p.save()
        order.save()
        return order

    def update(self, instance, validated_data):
        instance.items = validated_data.get('items', instance.image_url)
        instance.save()
        return instance

