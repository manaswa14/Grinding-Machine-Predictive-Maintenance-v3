#include <WiFi.h>
#include <HTTPClient.h>
#include <ModbusMaster.h>
#include <cstring>

#define MAX485_RE 21
#define MAX485_DE 22

ModbusMaster node;

// WiFi Credentials
const char* ssid = "Lee-Spring-Wireless";
const char* password = "7182362222";

// Flask Server
const char* serverName = "http://172.25.165.114:5000/data";

// ---------------------------
// MAX485 Control
// ---------------------------

void preTransmission() {
  digitalWrite(MAX485_RE, HIGH);
  digitalWrite(MAX485_DE, HIGH);
}

void postTransmission() {
  
  digitalWrite(MAX485_RE, LOW);
  digitalWrite(MAX485_DE, LOW);
}

// ---------------------------
// Setup
// ---------------------------

void setup() {

  Serial.begin(115200);
  delay(3000);

  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("================================");
  Serial.println("WiFi Connected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("================================");

  // Modbus Setup

  pinMode(MAX485_RE, OUTPUT);
  pinMode(MAX485_DE, OUTPUT);

  digitalWrite(MAX485_RE, LOW);
  digitalWrite(MAX485_DE, LOW);

  Serial2.begin(9600, SERIAL_8N1, 16, 17);

  node.begin(1, Serial2);

  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);

  Serial.println("Modbus Ready!");
}

// ---------------------------
// Main Loop
// ---------------------------

void loop() {

  uint8_t result = node.readInputRegisters(14, 24);

  if (result == node.ku8MBSuccess) {

    auto getFloat = [&](int index) {

      uint16_t r0 = node.getResponseBuffer(index);
      uint16_t r1 = node.getResponseBuffer(index + 1);

      uint32_t value = ((uint32_t)r1 << 16) | r0;

      float f;
      memcpy(&f, &value, sizeof(float));

      return f;
    };

    float voltage = getFloat(0);
    float current = getFloat(8);
    float pf = getFloat(14);

    // Temporary values
    float power = 0.502;
    float freq = 50.01;

    // ---------------------------
    // Serial Output
    // ---------------------------

    Serial.print("Voltage : ");
    Serial.print(voltage, 2);

    Serial.print(" V | Current : ");
    Serial.print(current, 2);

    Serial.print(" A | Power : ");
    Serial.print(power, 3);

    Serial.print(" kW | PF : ");
    Serial.print(pf, 3);

    Serial.print(" | Frequency : ");
    Serial.print(freq, 2);

    Serial.println(" Hz");

    // ---------------------------
    // Send JSON to Flask Server
    // ---------------------------

    if (WiFi.status() == WL_CONNECTED) {

      HTTPClient http;

      http.begin(serverName);

      http.addHeader("Content-Type", "application/json");

      String json = "{";
      json += "\"voltage\":" + String(voltage, 2) + ",";
      json += "\"current\":" + String(current, 2) + ",";
      json += "\"power\":" + String(power, 3) + ",";
      json += "\"pf\":" + String(pf, 3) + ",";
      json += "\"frequency\":" + String(freq, 2);
      json += "}";

      int httpResponseCode = http.POST(json);

      if (httpResponseCode == 200) {

        Serial.println("Data sent successfully!");

      } else {

        Serial.print("Failed to send. HTTP Error: ");
        Serial.println(httpResponseCode);

      }

      http.end();

    } else {

      Serial.println("WiFi Disconnected!");

    }

  } else {

    Serial.print("Modbus Read Failed. Error Code: ");
    Serial.println(result);

  }

  delay(2000);
}