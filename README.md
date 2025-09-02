# IP Tracking and Security System

A comprehensive Django application that provides IP tracking, geolocation, rate limiting, and security features.

## Features

- **IP Geolocation**: Automatic country and city detection
- **Request Logging**: Detailed request tracking with metadata
- **IP Blacklisting**: Block malicious or suspicious IPs
- **Rate Limiting**: Protect against abuse
- **Admin Interface**: Easy management of logs and blocked IPs
- **Caching**: Optimized performance with request caching

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/alx-backend-security.git
    cd alx-backend-security
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure your settings in `settings.py`:

    ```python
    INSTALLED_APPS = [
        # ...
        'ip_tracking',
    ]

    MIDDLEWARE = [
        # ...
        'ip_tracking.middleware.IPLoggingMiddleware',
    ]

    # Rate limiting settings
    RATELIMIT_VIEW = 'ip_tracking.views.rate_limit_error'
    RATELIMIT_ENABLE = True
    RATELIMIT_USE_CACHE = "default"
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

## Usage

### API Endpoints

#### Test Geolocation

```http
GET /ip-tracking/test-geo/
POST /ip-tracking/test-geo/
```

**Example Request:**

```bash
curl -X POST http://127.0.0.1:8000/ip-tracking/test-geo/ \
  -H "Content-Type: application/json" \
  -d '{"ip": "197.210.64.1"}'  # Ghana IP
```

**Example Response:**

```json
{
    "ip_address": "197.210.64.1",
    "country": "Ghana",
    "city": "Accra",
    "latitude": 5.55,
    "longitude": -0.2167
}
```

#### Rate Limited Login

```http
POST /ip-tracking/login/
```

**Rate Limits:**

- 10 requests/minute for authenticated users
- 5 requests/minute for anonymous users

### Management Commands

#### Block an IP Address

```bash
python manage.py block_ip 192.168.1.100 --reason "Suspicious activity"
```

### Admin Interface

Access the admin panel at `http://127.0.0.1:8000/admin/` to:

- View and manage request logs
- Block/unblock IP addresses
- Monitor system activity

## Testing

### Run Tests

```bash
python manage.py test ip_tracking
```

### Manual Testing

1. **Test Rate Limiting**

    ```bash
    # Test anonymous rate limit (5 requests/minute)
    for i in {1..6}; do
        curl http://127.0.0.1:8000/ip-tracking/test-geo/
        echo "---"
    done
    ```

2. **Test IP Blocking**

    ```bash
    # Block an IP
    python manage.py block_ip 192.168.1.100
    
    # Test blocked IP
    curl -H "X-Forwarded-For: 192.168.1.100" http://127.0.0.1:8000/ip-tracking/test-geo/
    ```

## Configuration

### Rate Limiting

Configure in `settings.py`:

```python
RATELIMIT_GROUP_HANDLERS = {
    'login': 'ip_tracking.ratelimit_handlers.login_handler',
    'geo_test': 'ip_tracking.ratelimit_handlers.geo_test_handler',
}
```

### Caching

Default uses local memory cache. For production, use Redis or Memcached:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## Security Considerations

- IP addresses are hashed before storage
- Rate limiting helps prevent brute force attacks
- Admin interface is protected by Django's authentication
- Sensitive endpoints require authentication

## License

This project is for educational purposes under the ALX ProDEV SE Program.
