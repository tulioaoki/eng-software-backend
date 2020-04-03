from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from core.tests import setUp
from ..accounts.models import CustomUser


class AccountsTest(APITestCase):

    def setUp(self):
        setUp(self)

    def test_login(self):
        self.client = APIClient()

        response = self.client.post("/v1.0/login", {"username": "admin", "password": "admin123"},
                                    header='content-type: application/json')
        response_content = json.loads(response.content.decode('utf-8'))
        self.token = response_content["data"]["token"]
        test_token = 'Token {}'.format(self.token)
        self.client.credentials(HTTP_AUTHORIZATION=test_token)
        # We want to make sure we have two users in the database..
        self.assertEqual(CustomUser.objects.count(), 3)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRelatedToken(APITestCase):
    def setUp(self):
        setUp(self)

    def test_create_user_using_post(self):

        data = {
            "username":"postuser",
            "password":"postpass",

        }
        self.client.post('/v1.0/register', data=data, format='json')
        self.assertEqual(4, CustomUser.objects.count())
        self.assertEqual(4, Token.objects.count())