from base import TestViewSetBase


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"

    test_task_info = {
        "title": "Test task title",
        "description": "Test task description",
        "deadline": "2023-05-01",
        "state": "new_task",
        "priority": 10,
        "assignee": None,
        "author": None,
        "tag": [],
    }

    @staticmethod
    def delete_keys(*args, data: dict):
        for key in args:
            data.pop(key)

    def test_create(self) -> None:
        task = self.create(self.test_task_info)
        self.delete_keys("created", "modified", data=task)
        expected_response = self.expected_details(task, self.test_task_info)
        assert task == expected_response

    def test_list(self):
        another_task = {
            "title": "Another test task title",
            "description": "Another test task description",
            "deadline": "2023-05-02",
            "state": "new_task",
            "priority": 9,
            "assignee": None,
            "author": None,
            "tag": [],
        }
        self.create(self.test_task_info)
        self.create(another_task)
        tasks = self.list()
        assert len(tasks) == 2
        for task in tasks:
            self.delete_keys("id", "modified", "created", data=task)
        assert tasks == [self.test_task_info, another_task]

    def test_retrieve(self):
        task = self.create(self.test_task_info)
        retrieved_task = self.retrieve(task["id"])
        assert task == retrieved_task

    def test_update(self):
        task = self.create(self.test_task_info)
        task.pop("modified")
        task["title"] = "Renamed title"
        updated_task = self.update(data=task, key=task["id"])
        updated_task.pop("modified")
        assert task == updated_task

    def test_delete(self):
        task = self.create(self.test_task_info)
        self.delete(task["id"])
        self.check_delete(task["id"])

    def test_unauthorized(self):
        self.check_unauthorized()
