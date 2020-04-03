from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.accounts.roles.models import Role
from core.accounts.roles.serializers import RolesSerializer
from core.utils.utilities import default_response, custom_permission_required


class ViewAllRoles(APIView):
    permission_classes = (IsAdminUser,)
    http_method_names = ['get',]

    @method_decorator(custom_permission_required(modulo='roles', perms=['leitor', 'editor', 'autor']))
    def get(self, request, format=None):
        objects = Role.objects.all()
        serializer = RolesSerializer(objects, many=True)
        return Response(default_response(code='get.roles.success',
                                         success=True,
                                         message='Role retornado com sucesso.',
                                         data=serializer.data,
                                         ), status=status.HTTP_200_OK)


class RoleDetail(APIView):
    permission_classes = (IsAdminUser,)
    http_method_names = ['get']

    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return default_response(code='get.roles.error',
                                    success=False,
                                    message='Role nao existe ou ja foi deletado.',
                                    )

    @method_decorator(custom_permission_required(modulo='roles', perms=['leitor', 'editor', 'autor']))
    def get(self, request, pk, format=None):
        objects = self.get_object(pk)
        if type(objects) == dict:
            return Response(objects, status.HTTP_404_NOT_FOUND)
        serializer = RolesSerializer(objects)
        return Response(default_response(code='get.roles.success',
                                         success=True,
                                         message='Role retornado com sucesso.',
                                         data=serializer.data,
                                         ), status.HTTP_200_OK)


class RolesPost(APIView):
    permission_classes = (IsAdminUser,)
    http_method_names = ['post', ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @method_decorator(custom_permission_required(modulo='roles', perms=['editor', ]))
    def post(self, request):

        serializer = RolesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(validated_data=request.data)
            if type(data) == str:
                return Response(default_response(code='post.roles.error',
                                                 success=False,
                                                 message='Role nao retornado com sucesso.',
                                                 data=serializer.error_messages,
                                                 )
                                , status=status.HTTP_400_BAD_REQUEST)
            return Response(default_response(code='create.roles.success',
                                             success=True,
                                             message='Role retornado com sucesso.',
                                             data=serializer.data,
                                             ), status=status.HTTP_201_CREATED, )
        return Response(default_response(code='post.roles.error',
                                         success=False,
                                         message='Role nao retornado com sucesso.',
                                         data=serializer.errors,
                                         ),
                        status=status.HTTP_400_BAD_REQUEST)
