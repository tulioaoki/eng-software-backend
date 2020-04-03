from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.accounts.models import CustomUser
from core.accounts.serializers import UserSerializer, UserInfoSerializer, \
    UserViewSerializer
from core.utils.utilities import default_response, custom_filter


class UserCreate(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def post(self,request, format=None):
      serializer = UserSerializer(data=request.data)
      if serializer.is_valid(raise_exception=ValueError):
          data = serializer.create(validated_data=request.data)
          if type(data) == str:
              return Response(default_response(code='post.users.error',
                                                 success=False,
                                                 message='User nao criado com successo.',
                                                 data={'detail':data}), status=status.HTTP_400_BAD_REQUEST)
          return Response(default_response(code='post.users.success',
                                         success=True,
                                         message='User criado com successo.',
                                         data=serializer.data),status=status.HTTP_201_CREATED)
      return Response(default_response(code='post.user.error',
                                                 success=False,
                                                 message='User nao criado com successo.',
                                                 data=serializer.error_messages),status=status.HTTP_400_BAD_REQUEST)



class ViewAllUsers(APIView):
    """Retorna todos os usuarios"""
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get',]

    def get_objects(self, request):
        objects = CustomUser.objects.all()
        obj = custom_filter(objects,request)
        return obj

    def get(self, request, format=None):
        objects = self.get_objects(request)
        serializer = UserSerializer(objects, many=True)
        return Response(default_response(code='get.users.success',
                                         success=True,
                                         message='User retornado com successo.',
                                         data=serializer.data,
                                         ), status=status.HTTP_200_OK)


class UsersGet(APIView):
    permission_classes = (IsAdminUser,)
    http_method_names = ['get','put']

    def get_object(self,pk):
        try:
            user = CustomUser.objects.get(id=pk)
            return user
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        objects = self.get_object(pk)
        serializer = UserInfoSerializer(objects)
        return Response(default_response(code='get.users.success',
                                         success=True,
                                         message='User retornado com successo.',
                                         data=serializer.data,
                                         ), status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        objects = self.get_object(pk)
        serializer = UserSerializer(objects, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(default_response(code='put.users.success',
                                         success=True,
                                         message='User editado com successo.',
                                         data=serializer.data,
                                         ), status=status.HTTP_201_CREATED)
        return Response(default_response(code='put.users.fail',
                                         success=True,
                                         message='User nao editado com successo.',
                                         data=serializer.errors,
                                         ),
                                         status=status.HTTP_400_BAD_REQUEST)


class MyProfile(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get_object(self):
        try:
            username = self.request.user
            user = CustomUser.objects.get(username=username)
            return user
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        objects = self.get_object()
        serializer = UserViewSerializer(objects)
        return Response(default_response(code='get.users.success',
                                         success=True,
                                         message='User retornado com successo.',
                                         data=serializer.data,
                                         ), status=status.HTTP_200_OK)
    def put(self, request, format=None):
        objects = self.get_object()
        serializer = UserSerializer(objects, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(default_response(code='put.users.success',
                                         success=True,
                                         message='User editado com successo.',
                                         data=serializer.data,
                                         ), status=status.HTTP_201_CREATED)
        return Response(default_response(code='put.users.fail',
                                         success=True,
                                         message='User nao editado com successo.',
                                         data=serializer.errors,
                                         ),
                                         status=status.HTTP_400_BAD_REQUEST)


class InactivateUser(APIView):
    """Desativa o usuario sem apaga-lo"""
    permission_classes = (IsAdminUser,)
    http_method_names = ['post']

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(username=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def post(self,request, format=None):
        username = request.data.get('username')
        user = self.get_object(username)
        if not user.is_active:
            return Response(default_response(code='inactivate.users.fail',
                                             success=False,
                                             message='Usuario ja esta inativo.',
                                             ), status=status.HTTP_400_BAD_REQUEST)
        user.deactivate()
        data = {"detail":username+' is now inactive.'}
        return Response(default_response(code='inactivate.users.success',
                                         success=True,
                                         message='Usuario inativado com successo.',
                                         data=data,
                                         ),status=status.HTTP_200_OK)


class ActivateUser(APIView):
    """Ativa o usuario"""
    permission_classes = (IsAdminUser,)
    http_method_names = ['post']

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(username=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def post(self,request, format=None):
        username = request.data.get('username')
        user = self.get_object(username)
        if user.is_active:
            return Response(default_response(code='activate.users.fail',
                                             success=False,
                                             message='Usuario ja esta ativo.',
                                             ), status=status.HTTP_400_BAD_REQUEST)
        user.activate()
        data = {"detail":username+' is now active.'}
        return Response(default_response(code='activate.users.success',
                                         success=True,
                                         message='Usuario ativado com successo.',
                                         data=data,
                                         ), status=status.HTTP_200_OK)


class ProfileDelete(APIView):
    permission_classes = (IsAdminUser,)
    http_method_names = ['delete']

    def get_object(self,pk):
        try:
            return CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def delete(self,request,pk,format=None):
        to_be_deleted = self.get_object(pk)
        to_be_deleted.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRole(APIView):
    """Returns the user's role"""
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get_object(self,request):
        try:
            username = request.username
            user = CustomUser.objects.get(username=username)
            user_role = user.role
            return user_role
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        role = self.get_object(request)
        resp = {}
        resp['role'] = role
        return Response(resp, status=status.HTTP_200_OK)
