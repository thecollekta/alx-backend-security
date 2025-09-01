# ip_tracking/middleware.py
from ip_tracking.models import RequestLog


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)

        # Log request details after response is processed
        ip_address = self.get_client_ip(request)

        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
            method=request.method,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
