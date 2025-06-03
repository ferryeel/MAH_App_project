from django.shortcuts import render

from rest_framework import viewsets
from .models import Metric, AlertRule
from .serializers import MetricSerializer, AlertRuleSerializer

class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.all()
    serializer_class = AlertRuleSerializer


def dashboard_view(request):
    return render(request, 'main/dashboard.html')  # Adjust path if different


