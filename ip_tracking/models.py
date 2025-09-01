# ip_tracking/models.py
from django.db import models
from django.utils import timezone


class RequestLog(models.Model):
    """
    Model representation to store details about each incoming request
    for auditing and analytics.
    """

    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=10)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"
