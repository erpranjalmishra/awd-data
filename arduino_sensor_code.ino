/*
Arduino Sensor Data Code
Upload this to your Arduino Uno to send sensor data to the Python script

This example shows how to format data for the Django dashboard.
Replace the dummy values with actual sensor readings.
*/

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  delay(2000); // Wait for serial connection
  Serial.println("Arduino Sensor Monitor Started");
}

void loop() {
  // Replace these with actual sensor readings
  float temperature = readTemperature();
  float humidity = readHumidity();
  float phLevel = readPH();
  float tdsValue = readTDS();
  
  // Send data in the format expected by Django
  Serial.print("temp:");
  Serial.print(temperature, 1);
  Serial.print(",humidity:");
  Serial.print(humidity, 1);
  Serial.print(",ph:");
  Serial.print(phLevel, 2);
  Serial.print(",tds:");
  Serial.println(tdsValue, 0);
  
  delay(2000); // Send data every 2 seconds
}

// Replace these functions with actual sensor reading code
float readTemperature() {
  // Example: DHT22 or DS18B20 temperature sensor
  // For testing, return a simulated value
  return 25.0 + random(-50, 100) / 10.0; // 20-30°C range
}

float readHumidity() {
  // Example: DHT22 humidity sensor
  // For testing, return a simulated value
  return 50.0 + random(-200, 200) / 10.0; // 30-70% range
}

float readPH() {
  // Example: pH sensor with analog reading
  // For testing, return a simulated value
  return 7.0 + random(-100, 100) / 100.0; // 6-8 pH range
}

float readTDS() {
  // Example: TDS sensor with analog reading
  // For testing, return a simulated value
  return 300 + random(-100, 200); // 200-500 ppm range
}

/*
ACTUAL SENSOR IMPLEMENTATION EXAMPLES:

1. Temperature (DHT22):
#include <DHT.h>
#define DHT_PIN 2
#define DHT_TYPE DHT22
DHT dht(DHT_PIN, DHT_TYPE);

float readTemperature() {
  return dht.readTemperature();
}

float readHumidity() {
  return dht.readHumidity();
}

2. pH Sensor (Analog):
#define PH_PIN A0
float readPH() {
  int sensorValue = analogRead(PH_PIN);
  float voltage = sensorValue * (5.0 / 1024.0);
  float ph = 3.5 * voltage; // Calibrate this formula
  return ph;
}

3. TDS Sensor (Analog):
#define TDS_PIN A1
float readTDS() {
  int sensorValue = analogRead(TDS_PIN);
  float voltage = sensorValue * (5.0 / 1024.0);
  float tds = voltage * 1000; // Calibrate this formula
  return tds;
}
*/