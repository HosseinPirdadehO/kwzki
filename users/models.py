from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    position = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='سمت')
    phone_number = models.CharField(
        max_length=11, unique=True, verbose_name='شماره تلفن', null=True)
    is_admin = models.BooleanField(default=False, verbose_name='نقش ادمین')
    is_active = models.BooleanField(
        default=True, verbose_name='فعال بودن حساب کاربری')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"
