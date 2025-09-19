from django.http import JsonResponse, HttpResponse
from datetime import datetime
import os

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
        <p><a href="/api/">API</a> | <a href="/health/">Health</a></p>
    </body>
    </html>
    """)

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

def health(request):
    """Ultra-minimal health check"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Server is running',
        'timestamp': datetime.now().isoformat(),
        'environment': {
            'debug': os.environ.get('DJANGO_DEBUG', 'not_set'),
            'allowed_hosts': os.environ.get('ALLOWED_HOSTS', 'not_set')
        }
    })