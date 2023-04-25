from http import HTTPStatus
from typing import Union, List

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    admin_attributes = None

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user(
            {**cls.admin_attributes, "is_staff": True, "is_superuser": True}
        )
        cls.client = APIClient()

    @staticmethod
    def create_api_user(params):
        return User.objects.create(**params)

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
        self.client.force_login(self.user)
        data = {key: value for key, value in data.items() if value is not None}
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def list(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def retrieve(self, key: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def update(self, key: Union[int, str], data: dict) -> dict:
        self.client.force_login(self.user)
        data = {key: value for key, value in data.items() if value is not None}
        response = self.client.put(self.detail_url(key), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def delete(self, key: Union[int, str]):
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(key))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        return response.data

    def check_delete(self, key: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.NOT_FOUND, response.content
        return response.data

    def check_unauthorized(self, args: List[Union[str, int]] = None) -> dict:
        self.client.logout()
        response = self.client.get(self.list_url(args))
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response.data
