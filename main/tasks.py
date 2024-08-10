from celery import shared_task
from .models import Subscription
from django.utils import timezone

@shared_task
def check_expired_subscriptions():
    expired_subscriptions = Subscription.objects.filter(end_date__lt=timezone.now().date())
    for subscription in expired_subscriptions:
        print(f"اشتراک {subscription} منقضی شده است.")