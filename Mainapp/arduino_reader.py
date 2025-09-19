import serial
import time
import threading
import json
import os
from datetime import datetime
import random

# Change COM port and baudrate as needed
SERIAL_PORT = 'COM6'  # Change this to your Arduino's COM port
BAUDRATE = 9600
DATA_FILE = 'Mainapp/latest_data.txt'
HISTORY_FILE = 'Mainapp/sensor_history.json'
MAX_HISTORY_POINTS = 100

latest_data = ''

def parse_arduino_data(raw_data):
    """Parse Arduino data and return structured format"""
    data = {
        'temperature': None,
        'humidity': None,
        'ph': None,
        'tds': None,
        'o2': None,
        'timestamp': datetime.now().isoformat()
    }
    
    if raw_data and raw_data.strip():
        # Handle your Arduino's current format: "TDS: 0.00 ppm | pH: 2.66 | Distance: 224.08 cm | Temp: 31.40 C | Humidity: 69.00 %"
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
        
        # Handle standard format: "temp:25.5,humidity:60.2,ph:7.1,tds:450"
        elif ',' in raw_data:
            parts = raw_data.split(',')
            for part in parts:
                if ':' in part:
                    key, value = part.split(':', 1)
                    try:
                        num_value = float(value.strip())
                        key = key.strip().lower()
                        if key in ['temp', 'temperature']:
                            data['temperature'] = num_value
                        elif key in ['humidity', 'hum']:
                            data['humidity'] = num_value
                        elif key == 'ph':
                            data['ph'] = num_value
                        elif key == 'tds':
                            data['tds'] = num_value
                    except ValueError:
                        continue
    return data

def save_to_history(parsed_data):
    """Save parsed data to history file"""
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []
    
    history.append(parsed_data)
    
    # Keep only last MAX_HISTORY_POINTS
    if len(history) > MAX_HISTORY_POINTS:
        history = history[-MAX_HISTORY_POINTS:]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def try_connect_arduino():
    """Try to connect to Arduino quickly - if fails, start dummy data immediately"""
    print(f"Trying to connect to COM6...")
    try:
        ser = serial.Serial('COM6', BAUDRATE, timeout=1)
        time.sleep(1)  # Short wait
        print(f"✅ Successfully connected to Arduino on COM6")
        return ser, 'COM6'
    except Exception as e:
        print(f"❌ Failed to connect to COM6: {e}")
        print("🔄 Starting dummy data immediately...")
        return None, None

def read_from_arduino():
    """Try to read real data from Arduino - if fails, immediately switch to dummy"""
    global latest_data
    
    ser, connected_port = try_connect_arduino()
    
    if ser is None:
        print("⚠️  No Arduino connection - using dummy data for testing")
        return False
    
    try:
        print(f"🔌 Reading data from Arduino on {connected_port}")
        print("📊 Expected format: temp:25.5,humidity:60.2,ph:7.1,tds:450")
        print("-" * 50)
        
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line and line != "Arduino Sensor Monitor Started":
                        latest_data = line
                        print(f"📥 Arduino: {line}")
                        
                        # Save raw data
                        with open(DATA_FILE, 'w') as f:
                            f.write(latest_data)
                        
                        # Parse and save structured data
                        parsed_data = parse_arduino_data(line)
                        save_to_history(parsed_data)
                        
                except UnicodeDecodeError:
                    continue
                    
            time.sleep(0.2)
            
    except Exception as e:
        print(f"❌ Error reading from Arduino: {e}")
        ser.close()
        return False

def create_dummy_data():
    """Create dummy data for testing when Arduino is not connected"""
    print("🤖 Generating realistic dummy sensor data...")
    print("📊 Format: Using your Arduino's actual format")
    print("-" * 50)
    
    while True:
        # Generate realistic dummy data
        dummy_temp = round(20 + random.uniform(-5, 15), 1)
        dummy_humidity = round(40 + random.uniform(-10, 20), 1)
        dummy_ph = round(6.5 + random.uniform(-1, 1.5), 2)
        dummy_tds = round(300 + random.uniform(-100, 200), 1)
        dummy_distance = round(200 + random.uniform(-50, 50), 2)
        dummy_o2 = round(random.uniform(85, 89), 1)
        
        # Create data in your Arduino's format
        raw_data = f"TDS: {dummy_tds} ppm | pH: {dummy_ph} | Distance: {dummy_distance} cm | Temp: {dummy_temp} C | Humidity: {dummy_humidity} % | O2: {dummy_o2} %"
        
        # Save raw data
        with open(DATA_FILE, 'w') as f:
            f.write(raw_data)
        
        # Parse and save structured data
        dummy_data = {
            'temperature': dummy_temp,
            'humidity': dummy_humidity,
            'ph': dummy_ph,
            'tds': dummy_tds,
            'o2': dummy_o2,
            'timestamp': datetime.now().isoformat()
        }
        save_to_history(dummy_data)
        
        print(f"🔄 DUMMY: Temp: {dummy_temp}°C | Humidity: {dummy_humidity}% | pH: {dummy_ph} | TDS: {dummy_tds}ppm | O2: {dummy_o2}%")
        time.sleep(2)

def main():
    print("\n" + "="*60)
    print("🚀 ARDUINO SENSOR DATA READER")
    print("="*60)
    
    # Try to read from real Arduino first, but fallback quickly
    arduino_connected = read_from_arduino()
    
    # If Arduino not connected, immediately use dummy data
    if not arduino_connected:
        create_dummy_data()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("🔄 Falling back to dummy data...")
        create_dummy_data()
