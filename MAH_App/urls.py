# urls.py inside your app (e.g. MAH_App/urls.py)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MetricViewSet, AlertRuleViewSet

router = DefaultRouter()
router.register(r'metrics', MetricViewSet)
router.register(r'alert-rules', AlertRuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
