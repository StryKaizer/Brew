#include <OneWire.h>
#include <DallasTemperature.h>
#include <aJSON.h>

// Data wire is plugged into pin 2 on the Arduino
# define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);



// Mapping
int ledGreen = 13;
int ledYellow = 12;
int heatRelay = 11; // Red LED atm

// Helpers
int incomingByte = 0; 
unsigned long lastPrint = 0;

aJsonStream serial_stream(&Serial);

void setup(void)
{
  pinMode(ledGreen, OUTPUT);
  pinMode(ledYellow, OUTPUT);
  pinMode(heatRelay, OUTPUT);
  
  // start serial port
  Serial.begin(9600);

  // Start up the temperature sensor library for DS18B20 sensor
  sensors.begin(); // IC Default 9 bit. If you have troubles consider upping it 12. Ups the delay giving the IC more time to process the temperature measurement
}


void loop(void)
{ 

  // Handle incoming requests
//  incomingByte = Serial.read();
//  switch (incomingByte) {
//    case 72:  // = H, Turn on Heat
//      digitalWrite(heatRelay, HIGH);
//      break;
//    case 104: // = H, Turn off Heat
//      digitalWrite(heatRelay, LOW);
//      break;
//  }
  
    if (serial_stream.available()) {
    /* First, skip any accidental whitespace like newlines. */
    serial_stream.skip();
  }

  if (serial_stream.available()) {
    /* Something real on input, let's take a look. */
    aJsonObject *msg = aJson.parse(&serial_stream);
    processMessage(msg);
    aJson.deleteItem(msg);
  }
  
    
  // Handle outgoing data
//  if (millis() - lastPrint > 1000) {  // Not sure if we need the 1sec delay
    
    aJsonObject *msg = getOutputJSON();
    aJson.print(msg, &serial_stream);
    Serial.println(); /* Add newline. */
    aJson.deleteItem(msg);
    lastPrint = millis();
//}
  
}


/* Process message like: { "pwm": { "8": 0, "9": 128 } } */
void processMessage(aJsonObject *msg)
{
  aJsonObject *heat = aJson.getObjectItem(msg, "heat");
  if (!heat) {
    Serial.println("no heat data");
    return;
  }else{
    Serial.println("yay");
  }
  if (heat->type != aJson_Int) {
    Serial.print("invalid data type ");
    Serial.print(heat->type, DEC);
    return;
  }
  analogWrite(heatRelay, heat->valueint);
}



aJsonObject *getOutputJSON()
{
  aJsonObject *msg = aJson.createObject();
  
  //PWM data
  aJsonObject *heat = aJson.createItem(digitalRead(heatRelay));
  aJson.addItemToObject(msg, "heat", heat);
  
  // Temperature sensor data
  sensors.requestTemperatures();
  aJsonObject *t1 = aJson.createItem(sensors.getTempCByIndex(0));
  aJson.addItemToObject(msg, "t1", t1);

  return msg;
}

