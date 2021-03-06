from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.carrosel.models import Carrosel
from core.carrosel.serializers import CarroselSerializer
from core.utils.utilities import default_response, custom_filter


class CarroselView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post',]

    def get_objects(self, request):
        objects = Carrosel.objects.all().order_by('-created_at')
        obj = custom_filter(objects, request)
        return obj

    def get(self, request, format=None):
        carrosel = self.get_objects(request)
        serializer = CarroselSerializer(carrosel, many=True)
        return Response(default_response(code='get.category.success',
                                         success=True,
                                         data=serializer.data,
                                         message="Carrosel retornado com sucesso."
                                         ), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CarroselSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(validated_data=request.data)
            if type(data) == str:
                return Response(default_response(code='get.category.error',
                                                 success=False,
                                                 message='Carrosel não retornado com sucesso.',
                                                 data={'detail':data},
                                                 )
                                ,status=status.HTTP_400_BAD_REQUEST)
            data = CarroselSerializer(data).data
            return Response(default_response(code='create.category.success',
                                         success=True,
                                         message='Carrosel retornado com sucesso.',
                                         data=data,
                                         ), status=status.HTTP_201_CREATED,)
        return Response(default_response(code='get.category.error',
                                         success=False,
                                         message='Carrosel não retornado com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)


class CarroselDetail(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'delete']

    def get_object(self,pk):
        try:
            return Carrosel.objects.get(pk=pk)
        except Carrosel.DoesNotExist:
             return default_response(code='get.category.error',
                                        success=False,
                                        message='Carrosel não existe ou ja foi deletado.',
                                        )

    def get(self, request,pk, format=None):
        objects = self.get_object(pk)
        if type(objects) == dict:
                return Response(objects, status.HTTP_404_NOT_FOUND)        
        serializer = CarroselSerializer(objects)        
        return Response(default_response(code='get.category.success',
                                         success=True,
                                         message='Carrosel retornada com sucesso.',
                                         data=serializer.data,
                                         ),status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        to_be_deleted = self.get_object(pk)
        to_be_deleted.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
