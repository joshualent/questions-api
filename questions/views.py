from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=True, methods=["post"])
    def upvote(self, request, pk=None, format=None):
        question = self.get_object()
        question.votes += 1
        question.save()
        return Response(self.get_serializer(question).data)


    @action(detail=True, methods=["post"])
    def toggle_answered(self, request, pk=None, format=None):
        question = self.get_object()
        question.answered = not question.answered
        question.save()
        return Response(self.get_serializer(question).data)
