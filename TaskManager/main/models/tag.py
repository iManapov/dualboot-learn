from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.title
