from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.accounts.models import CustomUser
from core.order.models import Order
from core.order.serializers import OrderSerializer
from core.utils.utilities import default_response, custom_filter


class OrderView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post',]

    def get_objects(self, request):
        u = CustomUser.objects.get(pk=request.user.id)
        if(u.is_superuser):
            objects = Order.objects.filter().order_by('-created_at')
        else:
            objects = Order.objects.filter(owner=u).order_by('-created_at')
        obj = custom_filter(objects, request)
        return obj

    def get(self, request, format=None):
        order = self.get_objects(request)
        serializer = OrderSerializer(order, many=True)
        return Response(default_response(code='get.order.success',
                                         success=True,
                                         data=serializer.data,
                                         message="Order retornado com sucesso."
                                         ), status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(validated_data=request.data, user=request.user)
            if type(data) == str:
                return Response(default_response(code='get.order.error',
                                                 success=False,
                                                 message='Order não retornado com sucesso.',
                                                 data={'detail':data},
                                                 )
                                ,status=status.HTTP_400_BAD_REQUEST)
            return Response(default_response(code='create.order.success',
                                         success=True,
                                         message='Order retornado com sucesso.',
                                         data=OrderSerializer(data=data).data,
                                         ), status=status.HTTP_201_CREATED,)
        return Response(default_response(code='get.order.error',
                                         success=False,
                                         message='Order não retornado com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'delete']

    def get_object(self,pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
             return default_response(code='get.order.error',
                                        success=False,
                                        message='Order não existe ou ja foi deletado.',
                                        )

    def get(self, request,pk, format=None):
        objects = self.get_object(pk)
        if type(objects) == dict:
                return Response(objects, status.HTTP_404_NOT_FOUND)        
        serializer = OrderSerializer(objects)        
        return Response(default_response(code='get.order.success',
                                         success=True,
                                         message='Order retornada com sucesso.',
                                         data=serializer.data,
                                         ),status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        to_be_deleted = self.get_object(pk)
        to_be_deleted.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
