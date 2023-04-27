from rest_framework import status
from typing import Union, List

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import User
from factory.django import DjangoModelFactory
from factory import PostGenerationMethodCall, Faker


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    password = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    token_url = reverse("token_obtain_pair")
    refresh_token_url = reverse("token_refresh")

    @staticmethod
    def create_user() -> User:
        return UserFactory.create()

    @staticmethod
    def create_super_user() -> User:
        return SuperUserFactory.create()

    def token_request(self, username: str = None, password: str = "password"):
        client = self.client_class()
        if not username:
            username = self.create_user().username
        return client.post(
            self.token_url, data={"username": username, "password": password}
        )

    def refresh_token_request(self, refresh_token: str):
        client = self.client_class()
        return client.post(self.refresh_token_url, data={"refresh": refresh_token})

    def get_refresh_token(self):
        response = self.token_request()
        return response.json()["refresh"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_super_user()

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        token = self.token_request(self.user.username)
        self.client.force_authenticate(self.user, token=token)
        data = {key: value for key, value in data.items() if value is not None}
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == status.HTTP_201_CREATED, response.content
        return response.json()

    def list(self, args: List[Union[str, int]] = None) -> dict:
        token = self.token_request(self.user.username)
        self.client.force_authenticate(self.user, token=token)
        response = self.client.get(self.list_url(args))
        assert response.status_code == status.HTTP_200_OK, response.content
        return response.json()

    def retrieve(self, key: Union[int, str]) -> dict:
        token = self.token_request(self.user.username)
        self.client.force_authenticate(self.user, token=token)
        response = self.client.get(self.detail_url(key))
        assert response.status_code == status.HTTP_200_OK, response.content
        return response.json()

    def update(self, key: Union[int, str], data: dict) -> dict:
        token = self.token_request(self.user.username)
        self.client.force_authenticate(self.user, token=token)
        data = {key: value for key, value in data.items() if value is not None}
        response = self.client.put(self.detail_url(key), data=data)
        assert response.status_code == status.HTTP_200_OK, response.content
        return response.json()

    def delete(self, key: Union[int, str]):
        token = self.token_request(self.user.username)
        self.client.force_authenticate(self.user, token=token)
        response = self.client.delete(self.detail_url(key))
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
        return response.data

    def check_delete(self, key: Union[int, str]) -> dict:
        token = self.token_request(self.user.username)
        self.client.force_authenticate(self.user, token=token)
        response = self.client.get(self.detail_url(key))
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        return response.data

    def check_unauthorized(self, args: List[Union[str, int]] = None) -> dict:
        self.client.logout()
        response = self.client.get(self.list_url(args))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.content
        return response.data
