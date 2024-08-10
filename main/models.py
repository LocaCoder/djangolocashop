# django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# local
from accounts.models import User
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from datetime import date
import datetime


class Category(MPTTModel):
    name = models.CharField(
        max_length=200,
        verbose_name=_('name')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children')
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class MPTTMeta:
        order_insertion_by = [
            'name',
        ]

        verbose_name = 'my_category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_parent_url(self):
        return reverse(
            'main:category_filter',
            args=[
                self.name
            ]
        )


class Package(models.Model):
    category = models.ManyToManyField(
        Category,
        related_name='cat_package',
    )
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )
    image = models.ImageField(
        null=True,
        blank=True
    )
    description = RichTextField(
        blank=True,
        null=True,

    )
    available = models.BooleanField(
        default=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    is_premium = models.BooleanField(
        default=False,
    )
    update = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = (
            'name',
        )

    def __str__(self):
        return f'category : {self.category} name : {self.name}'

    def get_absolute_url(self):
        return reverse(
            'main:package_detail',
            args=[
                self.id,
                self.slug,
            ]
        )

    def user_can_like(self, user):
        user_like = user.u_vote.filter(package=self)
        if user_like.exists():
            return True
        return False


class Subscription(models.Model):
    sub_time = {
        'one-month': 30,
        'two-month': 60,
        'three-month': 90,
    }
    name = models.CharField(
        max_length=200,
        default='premium'
    )
    sub_time_select: str = models.CharField(
        max_length=11,
        choices=sub_time
    )
    image = models.ImageField(
        null=True,
        blank=True,
    )
    price = models.IntegerField(
        null=True,
        blank=True
    )
    available = models.BooleanField(
        default=True,
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    update = models.DateTimeField(
        auto_now=True
    )


class SubscriptionBuy(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_sub'
    )
    sub_type = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='sub_type'
    )
    purchased = models.BooleanField(
        default=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    update = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'purchased',
        ]

    def is_active(self):
        from django.utils import timezone
        time_sub = Subscription.sub_time_select
        return self.created <= timezone.now().date() <= timezone.now().date()

    def __str__(self):
        return f'user : {self.user} subType: {self.sub_type} created : {self.created}'


class Comment(MPTTModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='u_commits',
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='p_commits'
    )
    content = models.TextField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = [
            'created_at',
        ]

    def __str__(self):
        return f'Comment by {self.id}'


class Vote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='u_vote'
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='p_vote'
    )

    class Mete:
        ordering = (
            'package',
        )

    def __str__(self):
        return f'{self.user} Liked :  {self.package.slug}'
