from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "text", "votes", "answered", "created_at")
        read_only_fields = ("id", "votes", "answered", "created_at")
