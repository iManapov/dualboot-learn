from base import TestViewSetBase


class TestTagViewSet(TestViewSetBase):
    basename = "tags"

    test_tag_info = {"title": "Test tag title"}

    def test_create(self) -> None:
        tag = self.create(self.test_tag_info)
        expected_response = self.expected_details(tag, self.test_tag_info)
        assert tag == expected_response

    def test_list(self):
        another_tag = {"title": "Another tag"}
        self.create(self.test_tag_info)
        self.create(another_tag)
        tags = self.list()
        assert len(tags) == 2
        for tag in tags:
            tag.pop("id")
        assert tags == [self.test_tag_info, another_tag]

    def test_retrieve(self):
        tag = self.create(self.test_tag_info)
        retrieved_tag = self.retrieve(tag["id"])
        assert tag == retrieved_tag

    def test_update(self):
        tag = self.create(self.test_tag_info)
        tag["title"] = "Renamed title"
        updated_tag = self.update(data=tag, key=tag["id"])
        assert tag == updated_tag

    def test_delete(self):
        tag = self.create(self.test_tag_info)
        self.delete(tag["id"])
        self.check_delete(tag["id"])

    def test_unauthorized(self):
        self.check_unauthorized()
