from rest_framework import serializers
from .models import Metric, AlertRule

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['id', 'name', 'unit', 'description']


class AlertRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRule
        fields = [
            'id', 'metric', 'threshold', 'comparison', 'is_active',
            'email', 'notify_sms', 'phone_number', 'created_at'
        ]

    def validate(self, data):
        if data.get('threshold', 0) < 0:
            raise serializers.ValidationError("Threshold must be non-negative.")

        if data.get('notify_sms') and not data.get('phone_number'):
            raise serializers.ValidationError("Phone number required for SMS alerts.")

        if not data.get('notify_sms') and not data.get('email'):
            raise serializers.ValidationError("At least one notification method required.")

        return data
