from base import TestViewSetBase, UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    test_user_info = {
        "username": "johntest",
        "first_name": "John",
        "last_name": "Test",
        "email": "test@test.com",
    }

    def test_create(self) -> None:
        user = self.create(self.test_user_info)
        expected_response = self.expected_details(user, self.test_user_info)
        assert user == expected_response

    def test_list(self):
        another_user = self.create_user()
        users = self.list()
        assert len(users) == 2
        assert [user["username"] for user in users] == [
            self.user.username,
            another_user.username,
        ]

    def test_retrieve(self):
        user = self.create(self.test_user_info)
        retrieved_user = self.retrieve(user["id"])
        assert user == retrieved_user

    def test_update(self):
        user = self.create(self.test_user_info)
        user["first_name"] = "Terry"
        updated_user = self.update(data=user, key=user["id"])
        assert user == updated_user

    def test_delete(self):
        user = self.create(self.test_user_info)
        self.delete(user["id"])
        self.check_delete(user["id"])

    def test_unauthorized(self):
        self.check_unauthorized()
