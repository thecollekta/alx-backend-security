# IP Tracking Middleware for Django

A lightweight and efficient IP tracking solution for Django applications that logs request details including IP addresses, timestamps, paths, and user agents.

## Features

- **Request Logging**: Automatically logs all incoming requests
- **IP Blacklisting**: Block malicious or suspicious IP addresses
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

### Request Logging

All incoming requests are automatically logged to the `RequestLog` model.

### IP Blacklisting

#### Using the Admin Interface

1. Go to the Django admin interface
2. Navigate to "Blocked IPs" under the "IP_TRACKING" section
3. Add new IP addresses to block with an optional reason

#### Using the Management Command

```bash
# Block an IP address
python manage.py block_ip 192.168.1.100 --reason "Suspicious activity"
```

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

Access logs through the Django admin interface or via the shell:

```python
from ip_tracking.models import RequestLog, BlockedIP

# Get all blocked IPs
blocked_ips = BlockedIP.objects.all()

# Check if an IP is blocked
is_blocked = BlockedIP.objects.filter(ip_address='192.168.1.100').exists()

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

The `BlockedIP` model contains the following fields:

- `ip_address`: Blocked IP address (unique)
- `created_at`: When the IP was blocked (auto-populated)
- `reason`: Optional reason for blocking the IP

## Security & Privacy

- IP addresses are stored in a dedicated database field with proper validation
- The middleware respects the `X-Forwarded-For` header for proxy scenarios
- No personally identifiable information is stored beyond the IP address and user agent
- Blocked IPs receive an immediate 403 Forbidden response
- Consider implementing data retention policies to automatically purge old logs

## Performance Considerations

- The middleware has minimal impact on request/response time
- Blacklist checks are performed before processing the request
- For high-traffic sites, consider:
  - Using a dedicated logging solution
  - Implementing request sampling for logging
  - Using database read replicas for log queries

## Management Commands

### block_ip

Blocks an IP address by adding it to the blacklist.

```bash
python manage.py block_ip <ip_address> [--reason REASON]
```

**Arguments:**

- `ip_address`: The IP address to block (required)
- `--reason`: Optional reason for blocking the IP

## License

This project is for educational purposes under the ALX ProDEV SE Program.
