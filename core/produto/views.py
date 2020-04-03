from django.core import serializers
from rest_framework import status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.produto.models import Product
from core.produto.serializers import ProductSerializer
from core.utils.utilities import default_response, custom_filter


class Produtos(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post',]

    def get_objects(self, request):
        objects = Product.objects.all().order_by('-created_at')
        obj = custom_filter(objects, request)
        return obj

    def get(self, request, format=None):
        product = self.get_objects(request)
        serializer = ProductSerializer(product, many=True)
        return Response(default_response(code='get.product.success',
                                         success=True,
                                         data=serializer.data,
                                         message="Produto retornado com sucesso."
                                         ), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(validated_data=request.data)
            if type(data) == str:
                return Response(default_response(code='get.product.error',
                                                 success=False,
                                                 message='Produto não retornado com sucesso.',
                                                 data={'detail':data},
                                                 )
                                ,status=status.HTTP_400_BAD_REQUEST)
            return Response(default_response(code='create.product.success',
                                         success=True,
                                         message='Produto retornado com sucesso.',
                                         data=serializers.serialize('json', [data, ]),
                                         ), status=status.HTTP_201_CREATED,)
        return Response(default_response(code='get.product.error',
                                         success=False,
                                         message='Produto não retornado com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)


class ProdutoDetail(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'delete']

    def get_object(self,pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
             return default_response(code='get.product.error',
                                        success=False,
                                        message='Produto não existe ou ja foi deletado.',
                                        )

    def get(self, request,pk, format=None):
        objects = self.get_object(pk)
        if type(objects) == dict:
                return Response(objects, status.HTTP_404_NOT_FOUND)        
        serializer = ProductSerializer(objects)        
        return Response(default_response(code='get.product.success',
                                         success=True,
                                         message='Produto retornada com sucesso.',
                                         data=serializer.data,
                                         ),status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        to_be_deleted = self.get_object(pk)
        to_be_deleted.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
