
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os
import json
from datetime import datetime
from .models  import Sensordata
def home(request):
    return render(request, 'index.html')

@csrf_exempt
def health_check(request):
    """Comprehensive health check endpoint"""
    try:
        # Test database connection
        db_status = "unknown"
        db_count = 0
        try:
            db_count = Sensordata.objects.count()
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        # Test file system
        file_status = "unknown"
        try:
            data_file = os.path.join(os.path.dirname(__file__), 'latest_data.txt')
            file_status = "exists" if os.path.exists(data_file) else "missing"
        except Exception as e:
            file_status = f"error: {str(e)}"
        
        return JsonResponse({
            'status': 'healthy',
            'message': 'Django server is running',
            'timestamp': datetime.now().isoformat(),
            'database': {
                'status': db_status,
                'record_count': db_count
            },
            'files': {
                'status': file_status
            },
            'environment': {
                'debug': os.environ.get('DJANGO_DEBUG', 'not_set'),
                'allowed_hosts': os.environ.get('ALLOWED_HOSTS', 'not_set')
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Health check failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }, status=500)

def arduino_data(request):
    data_file = os.path.join(os.path.dirname(__file__), 'latest_data.txt')
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            raw_data = f.read().strip()
        
        # Parse the data to get individual values
        parsed_data = parse_arduino_data_for_api(raw_data)
        
        return JsonResponse({
            'data': raw_data,
            'parsed': parsed_data,
            'timestamp': os.path.getmtime(data_file)
        })
    else:
        return JsonResponse({'data': '', 'parsed': {}, 'timestamp': None})

def parse_arduino_data_for_api(raw_data):
    """Parse Arduino data for API response"""
    data = {
        'temperature': None,
        'humidity': None,
        'ph': None,
        'tds': None,
        'o2': None,
        "deviceid":"vikaspal@123"
    }
    
    if raw_data and raw_data.strip():
        # Handle your Arduino's format: "TDS: 0.00 ppm | pH: 2.66 | Distance: 224.08 cm | Temp: 31.40 C | Humidity: 69.00 %"
        if '|' in raw_data:
            parts = raw_data.split('|')
            for part in parts:
                part = part.strip()
                if 'Temp:' in part:
                    try:
                        temp_str = part.split('Temp:')[1].strip().replace('C', '').strip()
                        data['temperature'] = float(temp_str)
                    except (ValueError, IndexError):
                        pass
                elif 'Humidity:' in part:
                    try:
                        hum_str = part.split('Humidity:')[1].strip().replace('%', '').strip()
                        data['humidity'] = float(hum_str)
                    except (ValueError, IndexError):
                        pass
                elif 'pH:' in part:
                    try:
                        ph_str = part.split('pH:')[1].strip()
                        data['ph'] = float(ph_str)
                    except (ValueError, IndexError):
                        pass
                elif 'TDS:' in part:
                    try:
                        tds_str = part.split('TDS:')[1].strip().replace('ppm', '').strip()
                        data['tds'] = float(tds_str)
                    except (ValueError, IndexError):
                        pass
                elif 'O2:' in part:
                    try:
                        o2_str = part.split('O2:')[1].strip().replace('%', '').strip()
                        data['o2'] = float(o2_str)
                    except (ValueError, IndexError):
                        pass
    return data

def sensor_history(request):
    history_file = os.path.join(os.path.dirname(__file__), 'sensor_history.json')
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []
    else:
        history = []
    
    sensor_type = request.GET.get('sensor', 'all')
    
    if sensor_type == 'all':
        return JsonResponse({'history': history})
    else:
        # Filter for specific sensor
        filtered_data = []
        for entry in history:
            if sensor_type in entry and entry[sensor_type] is not None:
                filtered_data.append({
                    'timestamp': entry['timestamp'],
                    'value': entry[sensor_type],
                    'sensor': sensor_type
                })
        return JsonResponse({'history': filtered_data, 'sensor': sensor_type})


@csrf_exempt
def apisensordata(request):
    """
    API endpoint for sensor data with comprehensive error handling
    """
    try:
        # Log request for debugging
        print(f"API Request: {request.method} from {request.META.get('REMOTE_ADDR', 'unknown')}")
        
        # Try to get data from database
        try:
            sensordata = Sensordata.objects.all().order_by('-id').first()
            if sensordata:
                data = {
                    'temperature': float(sensordata.temp),
                    'humidity': float(sensordata.humidity),
                    'ph': float(sensordata.phvalue),
                    'tds': float(sensordata.tds),
                    'o2': float(sensordata.o2) if sensordata.o2 is not None else None,
                    "deviceid": sensordata.deviceid if sensordata.deviceid else "vikaspal@123",
                    "timestamp": sensordata.timestamp.isoformat() if sensordata.timestamp else None,
                    "status": "success",
                    "data_source": "database"
                }
                print(f"Database data found: {data['temperature']}°C")
            else:
                raise Sensordata.DoesNotExist("No sensor data found")
                
        except Exception as db_error:
            print(f"Database error: {str(db_error)}")
            # Return dummy data when no real data is available
            data = {
                'temperature': 25.5,
                'humidity': 60.0,
                'ph': 7.0,
                'tds': 150.0,
                'o2': 21.0,
                "deviceid": "vikaspal@123",
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "data_source": "dummy",
                "warning": f"Database unavailable: {str(db_error)}"
            }
        
        return JsonResponse(data, status=200)
        
    except Exception as e:
        print(f"Critical API error: {str(e)}")
        # Return fallback data even on critical errors
        fallback_data = {
            'temperature': 22.0,
            'humidity': 55.0,
            'ph': 6.8,
            'tds': 120.0,
            'o2': 20.5,
            "deviceid": "vikaspal@123",
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "data_source": "fallback",
            "error": f"Critical error: {str(e)}"
        }
        return JsonResponse(fallback_data, status=200)  # Still return 200 to avoid 400 errors
