from rest_framework import serializers
from .models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(required=False)
    author = UserSerializer(required=False)
    tag = TagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "deadline",
            "state",
            "priority",
            "tag",
            "assignee",
            "author",
            "created",
            "modified",
        )
