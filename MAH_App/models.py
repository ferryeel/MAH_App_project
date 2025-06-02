from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Metric(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AlertRule(models.Model):
    COMPARISON_CHOICES = [
        ('>', 'Greater than'),
        ('<', 'Less than'),
        ('>=', 'Greater or equal'),
        ('<=', 'Less or equal'),
        ('==', 'Equal'),
    ]

    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='alert_rules')
    threshold = models.FloatField()
    comparison = models.CharField(max_length=2, choices=COMPARISON_CHOICES)
    is_active = models.BooleanField(default=True)

    # Notification settings
    email = models.EmailField(null=True, blank=True)
    notify_sms = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # --- Validate thresholds ---
        if self.threshold < 0:
            raise ValidationError("Threshold must be non-negative.")

        # Example: For some metrics, maximum threshold makes no sense
        if self.metric.name.lower() == "cpu usage" and self.threshold > 100:
            raise ValidationError("CPU usage threshold must be <= 100%.")

        # --- Validate notification settings ---
        if self.notify_sms and not self.phone_number:
            raise ValidationError("Phone number is required when SMS notifications are enabled.")

        if not self.email and not self.notify_sms:
            raise ValidationError("At least one notification method (email or SMS) must be set.")

    def __str__(self):
        return f"{self.metric.name} {self.comparison} {self.threshold}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['metric', 'threshold', 'comparison'],
                name='unique_alert_per_metric_rule'
            )
        ]
