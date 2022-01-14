
#include <ArduinoJson.h>
String incoming = "";   // for incoming serial string data
DynamicJsonDocument doc(250);

bool dobeeps = false; // init
int counter = 0;
int repeat = 0;
long bdelay = 0;
int frequency = 0;
long duration = 0;


void setup() {

  Serial.begin(115200);     // opens serial port, sets data rate to 115200 bps
  pinMode(2, INPUT);  //setup HW

}


void loop() {

  if (Serial.available() > 0) {

    // read the incoming string:
    incoming = Serial.readStringUntil('\n'); // Until LF
    deserializeJson(doc, incoming);          // Test json-string {"frequency":800, "duration":100, "delay":200,"repeat":10}
    JsonObject obj = doc.as<JsonObject>();
    frequency = obj["frequency"];
    duration = obj["duration"];
    bdelay = obj["delay"];
    repeat = obj["repeat"];

    counter = 0;
    dobeeps = true;

  }

  if (dobeeps) {

    if (digitalRead(2) == HIGH) { // peak received from BIOPAC AcqKnowledge

      if (counter < repeat) { 

        delay(bdelay);                 // Wait for delay
        tone(10, frequency, duration); //tone(pin, frequency, duration)
        counter++;                     // update counter
        
      }
      else {                   // counter >= repeat
        dobeeps = false;
        Serial.println("Done.");
      }
    }
  }
}
