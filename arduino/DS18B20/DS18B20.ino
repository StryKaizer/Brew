#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 2 on the Arduino
# define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);




int ledGreen = 13;
int ledYellow = 12;
int ledRed = 11;
int incomingByte = 0; 
void setup(void)
{
  pinMode(ledGreen, OUTPUT);
  pinMode(ledYellow, OUTPUT);
  pinMode(ledRed, OUTPUT);
  
  // start serial port
  Serial.begin(9600);

  // Start up the library
  sensors.begin(); // IC Default 9 bit. If you have troubles consider upping it 12. Ups the delay giving the IC more time to process the temperature measurement
}


void loop(void)
{ 
    digitalWrite(ledRed, HIGH);   // sets the LED on
  delay(1000); 
      digitalWrite(ledRed, LOW);   // sets the LED on
      incomingByte = Serial.read();
      Serial.println(incomingByte, DEC);
  delay(1000); 
  
  // call sensors.requestTemperatures() to issue a global temperature 
  // request to all devices on the bus
  sensors.requestTemperatures(); // Send the command to get temperatures
  
  Serial.print("{'S1':");
  Serial.print(sensors.getTempCByIndex(0)); // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
  Serial.println("}");
  
}

