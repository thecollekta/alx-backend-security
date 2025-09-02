# ip_tracking/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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


class BlockedIP(models.Model):
    """
    Model representation for storing blacklisted IP addresses that are
    forbidden from accessing the app.
    """

    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(
        blank=True, null=True, help_text="Reason for blocking this IP"
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this IP block is active"
    )

    class Meta:
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ip_address} (Blocked at: {self.created_at})"

    def save(self, *args, **kwargs):
        # Validate IP address
        try:
            self.full_clean()
        except ValidationError as e:
            raise ValidationError(_(f"Invalid IP address: {self.ip_address}")) from e
        super().save(*args, **kwargs)
