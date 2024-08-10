# django
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# local
from .managers import UserManager
# Third-party
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    phone_number = models.CharField(
        max_length=11,
        unique=True,
    )
    image = models.ImageField(

    )
    full_name = models.CharField(
        max_length=100
    )
    is_active = models.BooleanField(
        default=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    bio = models.TextField(
        null=True,
        blank=True
    )
    objects = UserManager(

    )
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = [
        'email',
        'full_name'
    ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def is_sub(self):
        from main.models import SubscriptionBuy
        if self.id == SubscriptionBuy.user.id:
            return True
        return False


class OtpCode(models.Model):
    phone_number = models.CharField(
        max_length=11,
        unique=True
    )
    code = models.PositiveSmallIntegerField(

    )
    created = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
