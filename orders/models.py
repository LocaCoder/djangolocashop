# django
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
# local
from main.models import Subscription
# Third-party


class Order(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='orders'
    )
    paid = models.BooleanField(
        default=False
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    discount = models.IntegerField(
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        ordering = (
            'paid',
            '-updated'
        )

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    price = models.IntegerField(
        null=True,
        blank=True,
    )

    def get_cost(self):
        return self.price

    def __str__(self):
        return str(self.id)


class Coupon(models.Model):
    code = models.CharField(
        max_length=30,
        unique=True
    )
    valid_form = models.DateTimeField(
        null=True,
        blank=True
    )
    valid_to = models.DateTimeField(
        null=True,
        blank=True
    )
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(90)],
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.code
