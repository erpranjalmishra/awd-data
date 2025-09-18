
from django.shortcuts import render
from django.http import JsonResponse
import os
import json
from .models  import Sensordata
def home(request):
    return render(request, 'index.html')

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


def apisensordata(request):
    try:
        sensordata = Sensordata.objects.all().order_by('-id').first()
        if sensordata:
            data = {
                'temperature': sensordata.temp,
                'humidity': sensordata.humidity,
                'ph': sensordata.phvalue,
                'tds': sensordata.tds,
                'o2': sensordata.o2,
                "deviceid": sensordata.deviceid if sensordata.deviceid else "vikaspal@123",
                "timestamp": sensordata.timestamp.isoformat() if sensordata.timestamp else None,
                "status": "success",
                "data_source": "database"
            }
        else:
            # Return dummy data when no real data is available
            from datetime import datetime
            data = {
                'temperature': 25.5,
                'humidity': 60.0,
                'ph': 7.0,
                'tds': 150.0,
                'o2': 21.0,
                "deviceid": "vikaspal@123",
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "data_source": "dummy"
            }
        
        return JsonResponse(data)
    except Exception as e:
        # Return dummy data even on database errors
        from datetime import datetime
        data = {
            'temperature': 22.0,
            'humidity': 55.0,
            'ph': 6.8,
            'tds': 120.0,
            'o2': 20.5,
            "deviceid": "vikaspal@123",
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "data_source": "fallback",
            "warning": f"Database error: {str(e)}"
        }
        return JsonResponse(data)
