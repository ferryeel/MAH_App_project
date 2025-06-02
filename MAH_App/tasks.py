import requests
from celery import shared_task
from .models import Metric

PROMETHEUS_URL = 'http://localhost:9090/api/v1/query'

@shared_task
def scrape_prometheus_and_save():
    # Example: get CPU usage
    response = requests.get(PROMETHEUS_URL, params={'query': 'up'})
    data = response.json()

    for result in data.get('data', {}).get('result', []):
        metric_name = result['metric'].get('__name__', 'unknown')
        value = result['value'][1]

        Metric.objects.create(name=metric_name, value=value)
