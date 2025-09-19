from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os

@csrf_exempt
def home(request):
    """Ultra-minimal home view"""
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>Arduino Dashboard</title></head>
    <body>
        <h1>Arduino Dashboard</h1>
        <p>Server is running!</p>
        <p>Time: """ + datetime.now().isoformat() + """</p>
        <p><a href="/api/">API</a> | <a href="/apidatasensor/">API Data Sensor</a> | <a href="/health/">Health</a></p>
    </body>
    </html>
    """)

@csrf_exempt
def api(request):
    """Ultra-minimal API view"""
    return JsonResponse({
        'status': 'ok',
        'message': 'API is working',
        'timestamp': datetime.now().isoformat(),
        'temperature': 25.5,
        'humidity': 60.0,
        'ph': 7.0,
        'tds': 150.0,
        'o2': 21.0,
        'deviceid': 'vikaspal@123'
    })

@csrf_exempt
def health(request):
    """Ultra-minimal health check"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Server is running',
        'timestamp': datetime.now().isoformat(),
        'request_info': {
            'method': request.method,
            'path': request.path,
            'host': request.get_host(),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'unknown')
        },
        'environment': {
            'debug': os.environ.get('DJANGO_DEBUG', 'not_set'),
            'allowed_hosts': os.environ.get('ALLOWED_HOSTS', 'not_set')
        }
    })