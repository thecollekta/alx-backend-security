# IP Tracking Middleware for Django

A lightweight and efficient IP tracking solution for Django applications that logs request details including IP addresses, timestamps, paths, and user agents.

## Features

- **Request Logging**: Automatically logs all incoming requests
- **IP Address Tracking**: Accurately captures client IP addresses, even behind proxies
- **Request Details**: Logs path, HTTP method, and user agent
- **Performance Optimized**: Minimal impact on request/response cycle
- **Security-First**: Properly handles and stores sensitive data

## Installation

1. Add `'ip_tracking'` to your `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = [
        # ...
        'ip_tracking',
    ]
    ```

2. Add the middleware to your `MIDDLEWARE` in `settings.py`:

    ```python
    MIDDLEWARE = [
        # ...
        'ip_tracking.middleware.IPLoggingMiddleware',
    ]
    ```

3. Run migrations:

    ```bash
    python manage.py makemigrations ip_tracking
    python manage.py migrate
    ```

## Usage

Once installed, the middleware will automatically log all incoming requests to the `RequestLog` model.

### Viewing Logs

You can access the logs through the Django admin interface or via the shell:

```python
from ip_tracking.models import RequestLog

# Get all logs
logs = RequestLog.objects.all()

# Get logs for a specific IP
ip_logs = RequestLog.objects.filter(ip_address='192.168.1.1')

# Get recent logs (most recent first)
recent_logs = RequestLog.objects.order_by('-timestamp')[:100]
```

### Admin Integration

The `RequestLog` model is registered in the admin interface by default. To access it:

1. Ensure you have the admin site enabled
2. Visit `/admin/ip_tracking/requestlog/`

## Data Model

The `RequestLog` model contains the following fields:

- `ip_address`: Client's IP address (supports both IPv4 and IPv6)
- `path`: Requested URL path
- `method`: HTTP method (GET, POST, etc.)
- `timestamp`: When the request was made (auto-populated)
- `user_agent`: Client's user agent string (if available)

## Security & Privacy

- IP addresses are stored in a dedicated database field with proper validation
- The middleware respects the `X-Forwarded-For` header for proxy scenarios
- No personally identifiable information is stored beyond the IP address and user agent
- Consider implementing data retention policies to automatically purge old logs

## Performance Considerations

- The middleware has minimal impact on request/response time
- Logging happens after the response is sent to the client
- For high-traffic sites, consider:
  - Using a dedicated logging solution
  - Implementing request sampling
  - Using database read replicas for log queries

## License

This project is for educational purposes under the ALX ProDEV SE Program.
