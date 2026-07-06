#include <ModbusMaster.h>

#define MAX485_RE 21
#define MAX485_DE 22

ModbusMaster node;

void preTransmission() {
  digitalWrite(MAX485_RE, HIGH);
  digitalWrite(MAX485_DE, HIGH);
}

void postTransmission() {
  digitalWrite(MAX485_RE, LOW);
  digitalWrite(MAX485_DE, LOW);
}

// Read a swapped IEEE754 float (CDAB)
float readSwappedFloat(uint16_t reg)
{
  uint8_t result = node.readInputRegisters(reg, 2);

  if (result != node.ku8MBSuccess)
  {
    Serial.print("Register ");
    Serial.print(reg);
    Serial.print(" Error = ");
    Serial.println(result);
    return NAN;
  }

  uint16_t r0 = node.getResponseBuffer(0);
  uint16_t r1 = node.getResponseBuffer(1);

  uint32_t value = ((uint32_t)r1 << 16) | r0;

  float f;
  memcpy(&f, &value, sizeof(float));

  return f;
}

void setup()
{
  Serial.begin(115200);

  pinMode(MAX485_RE, OUTPUT);
  pinMode(MAX485_DE, OUTPUT);

  digitalWrite(MAX485_RE, LOW);
  digitalWrite(MAX485_DE, LOW);

  Serial2.begin(9600, SERIAL_8N1, 16, 17);

  node.begin(1, Serial2);

  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);

  Serial.println("SELEC FINAL TEST");
}

void loop()
{
  uint8_t result = node.readInputRegisters(14, 24);

  if (result == node.ku8MBSuccess)
  {
    auto getFloat = [&](int index)
    {
      uint16_t r0 = node.getResponseBuffer(index);
      uint16_t r1 = node.getResponseBuffer(index + 1);

      uint32_t value = ((uint32_t)r1 << 16) | r0;

      float f;
      memcpy(&f, &value, sizeof(float));

      return f;
    };

    float voltage = getFloat(0);   // Reg 14-15
    float current = getFloat(8);   // Reg 22-23 (best match from our tests)
    float pf      = getFloat(14);  // Reg 28-29
    float power   = 0.502;         // Temporary until exact register confirmed
    float freq    = 50.01;         // Temporary until exact register added

    Serial.print(voltage, 2);
    Serial.print(",");

    Serial.print(current, 2);
    Serial.print(",");

    Serial.print(power, 3);
    Serial.print(",");

    Serial.print(pf, 3);
    Serial.print(",");

    Serial.println(freq, 2);
  }

  delay(2000);
}