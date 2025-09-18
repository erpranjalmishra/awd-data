
from Mainapp.views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/arduino/', arduino_data, name='arduino_data'),
    path('api/history/', sensor_history, name='sensor_history'),
    path("apidatasensor/",apisensordata,name="apidatasensor"),
   
]

