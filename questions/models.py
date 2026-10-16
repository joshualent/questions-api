from django.conf import settings
from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=300)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
