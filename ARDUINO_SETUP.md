# Arduino Connection Troubleshooting Guide

## Step 1: Connect Your Arduino
1. Connect Arduino Uno to your computer via USB cable
2. Upload the provided `arduino_sensor_code.ino` to your Arduino
3. Open Arduino IDE Serial Monitor to verify data output
4. Note the COM port (e.g., COM3, COM4, etc.)

## Step 2: Update COM Port
The Python script will try to auto-detect your Arduino, but you can manually set it:
1. Open `Mainapp/arduino_reader.py`
2. Change line: `SERIAL_PORT = 'COM3'` to your Arduino's COM port
3. Save the file

## Step 3: Check Arduino Code Output
Your Arduino should send data in this format:
```
temp:25.5,humidity:60.2,ph:7.1,tds:450
```

## Step 4: Run the Updated Script
```bash
C:/SIH2025/myproject/.venv/Scripts/python.exe Mainapp/arduino_reader.py
```

## Expected Output:
- **With Arduino Connected**: "Successfully connected to COM3" + real sensor data
- **Without Arduino**: "Using dummy data for testing" + simulated data

## Common Issues:

### 1. "Permission Denied" Error
- Close Arduino IDE Serial Monitor
- Close any other programs using the COM port
- Try running as administrator

### 2. "No module named 'serial'" Error
```bash
C:/SIH2025/myproject/.venv/Scripts/pip.exe install pyserial
```

### 3. Wrong COM Port
- Check Device Manager > Ports (COM & LPT)
- Look for "Arduino Uno" or "USB Serial Port"
- Update SERIAL_PORT in arduino_reader.py

### 4. No Data from Arduino
- Verify Arduino code is uploaded correctly
- Check Serial Monitor shows data output
- Ensure baud rate matches (9600)
- Try different USB cable

## Data Format Requirements:
The Arduino must send data exactly like this:
```
temp:TEMPERATURE,humidity:HUMIDITY,ph:PH_VALUE,tds:TDS_VALUE
```

Example:
```
temp:26.5,humidity:65.3,ph:7.2,tds:420
```

## Real Sensor Integration:
Replace the dummy functions in arduino_sensor_code.ino with:
- DHT22 for temperature/humidity
- pH sensor module for pH readings
- TDS sensor for water quality

## Testing Without Arduino:
The script automatically generates realistic dummy data if no Arduino is detected, so you can test the web interface immediately.