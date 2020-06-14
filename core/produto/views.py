from django.core import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from core.produto.models import ProductImage, Product
from core.produto.serializers import ProductImageSerializer, ProductSerializer, ProductEditSerializer
from core.utils.utilities import default_response, custom_filter, paginated_response_dict, ObjectNotFound


class Produtos(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post',]

    def get_objects(self, request):
        objects = Product.objects.all().order_by('-created_at')
        obj = custom_filter(objects, request)
        return obj

    def get(self, request, format=None):
        items = self.get_objects(request)
        pagination_data = paginated_response_dict(items, request)
        if pagination_data is None:
            Response(default_response(code='get.product.success',
                                      success=True,
                                      data=[],
                                      message="Lista vazia.",
                                      pagination_data=None,
                                      ), status=status.HTTP_200_OK)
        serializer = ProductSerializer(pagination_data.get('objects'), many=True)
        return Response(default_response(code='get.product.success',
                                         success=True,
                                         data=serializer.data,
                                         message="Produto retornado com sucesso.",
                                         pagination_data=pagination_data,
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
            data = Product.objects.get(pk=data.id)
            return Response(default_response(code='create.product.success',
                                         success=True,
                                         message='Produto retornado com sucesso.',
                                         data=ProductSerializer(data).data,
                                         ), status=status.HTTP_201_CREATED,)
        return Response(default_response(code='get.product.error',
                                         success=False,
                                         message='Produto não retornado com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)


class ProdutoDetail(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'delete', 'put']

    def get_object(self,pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
             return default_response(code='get.product.error',
                                        success=False,
                                        message='Produto não existe ou ja foi deletado.',
                                        )

    def put(self, request, pk, format=None):
        objects = self.get_object(pk)
        serializer = ProductEditSerializer(objects, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = ProductSerializer(self.get_object(pk)).data
            return Response(default_response(code='put.products.success',
                                         success=True,
                                         message='Product editado com successo.',
                                         data=data,
                                         ), status=status.HTTP_201_CREATED)
        return Response(default_response(code='put.products.fail',
                                         success=True,
                                         message='Product nao editado com successo.',
                                         data=serializer.errors,
                                         ),
                                         status=status.HTTP_400_BAD_REQUEST)


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


class ProductImageView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post',]

    def get_objects(self, request):
        objects = ProductImage.objects.all().order_by('-created_at')
        obj = custom_filter(objects, request)
        return obj

    def get(self, request, format=None):
        productImage = self.get_objects(request)
        serializer = ProductImageSerializer(productImage, many=True)
        return Response(default_response(code='get.productImage.success',
                                         success=True,
                                         data=serializer.data,
                                         message="ProductImage retornado com sucesso."
                                         ), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(validated_data=request.data)
            if type(data) == str:
                return Response(default_response(code='get.productImage.error',
                                                 success=False,
                                                 message='ProductImage não retornado com sucesso.',
                                                 data={'detail':data},
                                                 )
                                ,status=status.HTTP_400_BAD_REQUEST)
            return Response(default_response(code='create.productImage.success',
                                         success=True,
                                         message='ProductImage retornado com sucesso.',
                                         data=serializers.serialize('json', [data, ]),
                                         ), status=status.HTTP_201_CREATED,)
        return Response(default_response(code='get.productImage.error',
                                         success=False,
                                         message='ProductImage não retornado com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)


class ProductImageDetail(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'delete']

    def get_object(self,pk):
        try:
            return ProductImage.objects.get(pk=pk)
        except ProductImage.DoesNotExist:
             return default_response(code='get.productImage.error',
                                        success=False,
                                        message='ProductImage não existe ou ja foi deletado.',
                                        )

    def get(self, request,pk, format=None):
        objects = self.get_object(pk)
        if type(objects) == dict:
                return Response(objects, status.HTTP_404_NOT_FOUND)
        serializer = ProductImageSerializer(objects)
        return Response(default_response(code='get.productImage.success',
                                         success=True,
                                         message='ProductImage retornada com sucesso.',
                                         data=serializer.data,
                                         ),status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        to_be_deleted = self.get_object(pk)
        to_be_deleted.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post',]

    def get_objects(self, request):
        objects = Product.objects.filter(offer=True).order_by('-created_at')
        obj = custom_filter(objects, request)
        return obj

    def get(self, request, format=None):
        product = self.get_objects(request)
        serializer = ProductSerializer(product, many=True)
        return Response(default_response(code='get.offer.success',
                                         success=True,
                                         data=serializer.data,
                                         message="Oferta retornado com sucesso."
                                         ), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(validated_data=request.data)
            if type(data) == str:
                return Response(default_response(code='get.product.error',
                                                 success=False,
                                                 message='Oferta não retornado com sucesso.',
                                                 data={'detail':data},
                                                 )
                                ,status=status.HTTP_400_BAD_REQUEST)
            return Response(default_response(code='create.product.success',
                                         success=True,
                                         message='Oferta retornada com sucesso.',
                                         data=serializers.serialize('json', [data, ]),
                                         ), status=status.HTTP_201_CREATED,)
        return Response(default_response(code='get.offer.error',
                                         success=False,
                                         message='Oferta não retornada com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)


class OfferDetail(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'delete']

    def get_object(self,pk):
        try:
            return Product.objects.filter(offer=True).get(pk=pk)
        except Product.DoesNotExist:
             return default_response(code='get.offer.error',
                                        success=False,
                                        message='Oferta não existe ou ja foi deletado.',
                                        )

    def get(self, request,pk, format=None):
        objects = self.get_object(pk)
        if type(objects) == dict:
                return Response(objects, status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(objects)
        return Response(default_response(code='get.offer.success',
                                         success=True,
                                         message='Oferta retornada com sucesso.',
                                         data=serializer.data,
                                         ),status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        to_be_deleted = self.get_object(pk)
        to_be_deleted.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProdutosRecentes(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get',]

    def get_objects(self, request):
        from datetime import datetime, timedelta
        last_month = datetime.today() - timedelta(days=30)
        objects = Product.objects.filter(created_at__gte=last_month).order_by('-created_at')
        obj = custom_filter(objects, request)
        return obj

    def get(self, request, format=None):
        items = self.get_objects(request)
        pagination_data = paginated_response_dict(items, request)
        if pagination_data is None:
            Response(default_response(code='get.product.success',
                                      success=True,
                                      data=[],
                                      message="Lista Vazia.",
                                      pagination_data=None,
                                      ), status=status.HTTP_200_OK)
        serializer = ProductSerializer(pagination_data.get('objects'), many=True)
        return Response(default_response(code='get.product.success',
                                         success=True,
                                         data=serializer.data,
                                         message="Produto retornado com sucesso.",
                                         pagination_data=pagination_data,
                                         ), status=status.HTTP_200_OK)