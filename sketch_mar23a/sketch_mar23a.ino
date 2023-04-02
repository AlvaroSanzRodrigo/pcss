#include <Adafruit_SSD1306.h>
#include <Wire.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


void setup() {
  Serial.begin(9600);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3D);  // initialize with the I2C addr 0x3C (for the 128x64)
  display.clearDisplay();     
  
}

float f;
char x[8];

void loop() {
  if(Serial.available()){
    f = Serial.parseFloat();
    display.setTextSize(1);                  // set text size
    display.setTextColor(SSD1306_WHITE);     // set text color
    display.setCursor(0,0);   
    dtostrf(f,5,2,x);
    Serial.println(x);               // set cursor position
    display.println(x);        // print text
    display.display();                       // show the text on display
    delay(1000);                             // wait for a second
    display.clearDisplay();  
  }   
}