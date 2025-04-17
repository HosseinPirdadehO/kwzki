from django.db import models
from django.conf import settings

# Create your models here.


class WorkSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None


class BreakSession(models.Model):
    work_session = models.ForeignKey(
        WorkSession, on_delete=models.CASCADE, related_name='breaks')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None
