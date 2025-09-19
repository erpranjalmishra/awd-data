
from Mainapp.views import home, api, health
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('api/', api, name='api'),
    path('health/', health, name='health'),
]

