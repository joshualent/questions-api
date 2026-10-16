from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from questions.views import QuestionViewSet

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="question")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
