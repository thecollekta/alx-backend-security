# ip_tracking/views.py
import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class TestGeoLocationView(View):
    """
    Test endpoint to verify IP geolocation
    GET: Returns the request's geolocation data
    POST: Allows testing with custom X-Forwarded-For header
    """

    def get(self, request):
        ip = self.get_client_ip(request)
        return JsonResponse(
            {
                "ip_address": ip,
                "method": request.method,
                "path": request.path,
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "geo_headers": {
                    "x-forwarded-for": request.META.get("HTTP_X_FORWARDED_FOR"),
                    "remote_addr": request.META.get("REMOTE_ADDR"),
                },
            }
        )

    def post(self, request):
        data = json.loads(request.body)
        ip = data.get("ip", "")

        # Create a custom request with the specified IP
        request.META["HTTP_X_FORWARDED_FOR"] = ip
        return self.get(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
