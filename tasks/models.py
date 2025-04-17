from django.db import models
from django.conf import settings

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان تسک")
    description = models.TextField(verbose_name="توضیحات")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_tasks", verbose_name="کاربر دریافت‌کننده")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_tasks", verbose_name="ایجاد شده توسط")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ایجاد")
    is_completed = models.BooleanField(
        default=False, verbose_name="وضعیت انجام")
    submitted_text = models.TextField(
        blank=True, null=True, verbose_name="متن ارسال شده توسط کاربر")

    def __str__(self):
        return f"{self.title} - {self.assigned_to}"
