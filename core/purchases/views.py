from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.purchases.models import ItemProduct
from core.purchases.serializers import ItemProductSerializer
from core.utils.utilities import default_response


class CartView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get','post']


    def get(self, request, format=None):
        user = request.user
        data = ItemProductSerializer(user.cart.all(), many=True).data
        return Response(default_response(code='get.cart.success',
                                         success=True,
                                         message='Listou carrinho com successo.',
                                         data=data,
                                         ), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemProductSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(validated_data=request.data)
            user = request.user
            user.cart.add(data)
            user.save()
            if type(data) == str:
                return Response(default_response(code='get.item.error',
                                                 success=False,
                                                 message='Item não retornado com sucesso.',
                                                 data={'detail': data},
                                                 )
                                , status=status.HTTP_400_BAD_REQUEST)
            s = ItemProductSerializer(data=user.cart.all(), many=True)
            s.is_valid()
            return Response(default_response(code='create.item.success',
                                             success=True,
                                             message='Item retornada com sucesso.',
                                             data=s.data,
                                             ), status=status.HTTP_201_CREATED, )
        return Response(default_response(code='get.offer.error',
                                         success=False,
                                         message='Item não retornada com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)


class CartEdit(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put','delete']

    def get_item(self, pk):
        try:
            return ItemProduct.objects.get(id=pk)
        except:
            raise Http404

    def delete(self, request, pk, format=None):
        to_be_deleted = self.get_item(pk)
        to_be_deleted.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        objects = self.get_item(pk)
        serializer = ItemProductSerializer(objects, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(default_response(code='put.items.success',
                                         success=True,
                                         message='Item editado com successo.',
                                         data=serializer.data,
                                         ), status=status.HTTP_201_CREATED)
        return Response(default_response(code='put.items.fail',
                                         success=True,
                                         message='Item nao editado com successo.',
                                         data=serializer.errors,
                                         ),
                                         status=status.HTTP_400_BAD_REQUEST)

