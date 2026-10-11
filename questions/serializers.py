from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField(source="votes.count", read_only=True)
    has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("id", "text", "votes", "has_voted", "answered", "created_at")
        read_only_fields = ("id", "votes", "answered", "created_at")

    def get_has_voted(self, question):
        user = self.context["request"].user
        return question.votes.filter(pk=user.pk).exists()
