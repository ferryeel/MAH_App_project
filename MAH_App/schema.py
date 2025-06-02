import graphene
from graphene_django.types import DjangoObjectType
from .models import Metric, AlertRule

class MetricType(DjangoObjectType):
    class Meta:
        model = Metric
        fields = ("id", "name", "unit", "description")


class AlertRuleType(DjangoObjectType):
    class Meta:
        model = AlertRule
        fields = (
            "id", "metric", "threshold", "comparison", "is_active",
            "email", "notify_sms", "phone_number", "created_at"
        )


class Query(graphene.ObjectType):
    all_metrics = graphene.List(MetricType)
    all_alert_rules = graphene.List(AlertRuleType)
     # Fetch all metrics
    all_metrics = graphene.List(MetricType)

    # Fetch all active alert rules
    active_alert_rules = graphene.List(AlertRuleType)

    # Fetch alert rules by metric ID (argument)
    alert_rules_by_metric = graphene.List(AlertRuleType, metric_id=graphene.Int(required=True))

    # Count of metrics
    metrics_count = graphene.Int()

    # Count of active alert rules
    active_alert_rules_count = graphene.Int()

    # Resolvers
    def resolve_all_metrics(root, info):
        return Metric.objects.all()

    def resolve_active_alert_rules(root, info):
        return AlertRule.objects.filter(is_active=True)

    def resolve_alert_rules_by_metric(root, info, metric_id):
        return AlertRule.objects.filter(metric_id=metric_id)

    def resolve_metrics_count(root, info):
        return Metric.objects.count()

    def resolve_active_alert_rules_count(root, info):
        return AlertRule.objects.filter(is_active=True).count()
   


class CreateMetric(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        unit = graphene.String(required=True)
        description = graphene.String()

    metric = graphene.Field(MetricType)

    def mutate(self, info, name, unit, description=None):
        metric = Metric(name=name, unit=unit, description=description or "")
        metric.full_clean()  # optional: model validation
        metric.save()
        return CreateMetric(metric=metric)


class Mutation(graphene.ObjectType):
    create_metric = CreateMetric.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
