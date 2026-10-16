from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAdminUser()]

        return super().get_permissions()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_vote(self, request, pk=None, format=None):
        question = self.get_object()
        has_voted = question.votes.filter(pk=request.user.pk).exists()

        if has_voted:
            question.votes.remove(request.user)
        else:
            question.votes.add(request.user)

        return Response(self.get_serializer(question).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def toggle_answered(self, request, pk=None, format=None):
        question = self.get_object()
        question.answered = not question.answered
        question.save()
        return Response(self.get_serializer(question).data)
