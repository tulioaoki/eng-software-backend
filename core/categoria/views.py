from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.categoria.models import Category
from core.categoria.serializers import CategorySerializer
from core.utils.utilities import default_response, custom_filter


class Categorias(APIView):
    permission_classes = (IsAuthenticated, AllowAny)
    http_method_names = ['get', 'post',]

    def get_objects(self, request):
        objects = Category.objects.all().order_by('-created_at')
        obj = custom_filter(objects, request)
        return obj

    def get(self, request, format=None):
        Category = self.get_objects(request)
        serializer = CategorySerializer(Category, many=True)
        return Response(default_response(code='get.category.success',
                                         success=True,
                                         data=serializer.data,
                                         message="Categoria retornado com sucesso."
                                         ), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(validated_data=request.data)
            if type(data) == str:
                return Response(default_response(code='get.category.error',
                                                 success=False,
                                                 message='Categoria não retornado com sucesso.',
                                                 data={'detail':data},
                                                 )
                                ,status=status.HTTP_400_BAD_REQUEST)
            return Response(default_response(code='create.category.success',
                                         success=True,
                                         message='Categoria retornado com sucesso.',
                                         data=data,
                                         ), status=status.HTTP_201_CREATED,)
        return Response(default_response(code='get.category.error',
                                         success=False,
                                         message='Categoria não retornado com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)


class CategoriaDetail(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'delete']

    def get_object(self,pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
             return default_response(code='get.category.error',
                                        success=False,
                                        message='Categoria não existe ou ja foi deletado.',
                                        )

    def get(self, request,pk, format=None):
        objects = self.get_object(pk)
        if type(objects) == dict:
                return Response(objects, status.HTTP_404_NOT_FOUND)        
        serializer = CategorySerializer(objects)        
        return Response(default_response(code='get.category.success',
                                         success=True,
                                         message='Categoria retornada com sucesso.',
                                         data=serializer.data,
                                         ),status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        to_be_deleted = self.get_object(pk)
        to_be_deleted.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
