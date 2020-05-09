from rest_framework import serializers

from core.carrosel.models import Carrosel, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url", "base_64", "created_at", "updated_at", ]

    def create(self, validated_data):
        image = Image.objects.create(
            url=validated_data.get('url'),
            base_64=validated_data.get('base_64'),
        )
        return image

    def update(self, instance, validated_data):
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.base_64 = validated_data.get('base_64', instance.base_64)
        instance.save()
        return instance

class CarroselSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Carrosel
        fields = '__all__'

    def create(self, validated_data):
        images = validated_data.get('images')
        carrosel = Carrosel.objects.create(
            name=validated_data.get('name'),
        )

        if carrosel and images is not None:
            for i in images:
                img = ImageSerializer.create(ImageSerializer(), validated_data=i)
                carrosel.images.add(img)
        carrosel.save()
        return carrosel

    def update(self, instance, validated_data):
        instance.images = validated_data.get('images', instance.image_url)
        instance.save()
        return instance

