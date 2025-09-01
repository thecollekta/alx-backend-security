from django.contrib import admin

from .models import RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "path", "method", "timestamp", "user_agent_short")
    list_filter = ("method", "timestamp")
    search_fields = ("ip_address", "path", "user_agent")
    readonly_fields = ("ip_address", "path", "method", "timestamp", "user_agent")
    date_hierarchy = "timestamp"
    list_per_page = 50

    def user_agent_short(self, obj):
        """Display a shortened version of the user agent"""
        if obj.user_agent:
            return (
                obj.user_agent[:50] + "..."
                if len(obj.user_agent) > 50
                else obj.user_agent
            )
        return "-"

    user_agent_short.short_description = "User Agent (short)"

    def has_add_permission(self, request):
        """Prevent manual addition of log entries"""
        return False

    def has_change_permission(self, request, obj=None):
        """Prevent modification of log entries"""
        return False
