
from Mainapp.views import home, api, health
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('api/', api, name='api'),
    path('apidatasensor/', api, name='apidatasensor'),  # Add the missing endpoint
    path('health/', health, name='health'),
]

