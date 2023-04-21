from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from .tag import Tag


class Task(models.Model):
    class States(models.TextChoices):
        NEW = "new_task"
        DEVELOPMENT = "in_development"
        QA = "in_qa"
        REVIEW = "in_code_review"
        RELEASE_READY = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True)
    state = models.CharField(max_length=255, default=States.NEW, choices=States.choices)
    priority = models.IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tag = models.ManyToManyField(Tag)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignee",
        null=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author",
        null=True,
    )

    def __str__(self):
        return self.title
