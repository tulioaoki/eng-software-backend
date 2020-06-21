import random
import string

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.accounts.models import CustomUser
from core.loginAndRegister.utils import forgot_password_email
from core.utils.utilities import default_response


class CustomLogin(ObtainAuthToken,APIView,):
    http_method_names = ['post','get']
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = {'token': token.key,'user':user.username, 'is_admin':(user.is_superuser or user.is_admin)}
        return Response(default_response(code='post.login.success',
                                         success=True,
                                         message='Login realizado com sucesso.',
                                         data=data,
                                         status_code=200,
                                         ), status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        try:
            temp_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))#generates a random password
            email = request.data.get('email')
            try:
                user = CustomUser.objects.get(username=email)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            user.set_password(temp_password)
            user.save()
            forgot_password_email(email,temp_password)
            return Response(status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ChangePassword(APIView):
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        try:
            token = request.user.auth_token
            token_user = Token.objects.get(key=token).user
            if token_user.check_password(password):
                token_user.set_password(new_password)
                token_user.save()
                return Response(default_response(data='success',message="Senha alterada com sucesso.",
                                                 status_code=200,code="change-password.success",success=True),status=status.HTTP_200_OK)
            else:
                return Response("username and password don't match", status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response('username not found', status=status.HTTP_400_BAD_REQUEST)
        except Token.DoesNotExist:
            return Response('Invalid token', status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        data = {"data":"Logout succeeded"}
        return Response(default_response(code='get.logout.success',
                                         success=True,
                                         message='Logout realizado com sucesso.',
                                         data=data,
                                         ), status=status.HTTP_200_OK)


class CheckAuth(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()

    def get(self, request, format=None):
        # checks if the token exists and is valid
        user = request.user
        token = user.auth_token
        if Token and token in Token.objects.all():
            return Response(default_response(code='get.auth.success',
                                             success=True,
                                             message='Autenticado',
                                             data={"logged":"ok", 'is_admin':(user.is_superuser or user.is_admin)},
                                             ), status=status.HTTP_200_OK)
        else:
            return Response(default_response(code='get.auth.fail',
                                             success=True,
                                             message='fail',
                                             data={"logged": False, 'is_admin': (user.is_superuser or user.is_admin)},
                                             ), status=status.HTTP_404_NOT_FOUND)


