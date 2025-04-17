from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("شماره تلفن باید وارد شود.")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('سوپر یوزر باید is_staff=True باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('سوپر یوزر باید is_superuser=True باشد.')

        return self.create_user(phone_number, password, **extra_fields)


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

    objects = CustomUserManager()  # حالا بدون خطا

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"
