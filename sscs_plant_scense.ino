#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define LDRPIN A0

DHT dht(DHTPIN, DHTTYPE);

LiquidCrystal_I2C lcd(0x27,16,2);


void setup()
{
  Serial.begin(9600);

  dht.begin();

  lcd.begin();
  lcd.backlight();

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("PlantSense");
  lcd.setCursor(0,1);
  lcd.print("Ready");

  delay(2000);
}


void loop()
{
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int light = analogRead(LDRPIN);


  // Send sensors to Python

  if(!isnan(temperature) && !isnan(humidity))
  {
    Serial.print(temperature);
    Serial.print(",");
    Serial.print(humidity);
    Serial.print(",");
    Serial.println(light);
  }



  // Receive recommendation from Python

  if(Serial.available())
{
  String message = Serial.readStringUntil('\n');

  int comma = message.indexOf(',');

  String plant = message.substring(0, comma);
  String score = message.substring(comma + 1);


  lcd.clear();

  lcd.setCursor(0,0);
  lcd.print("Best:");
  lcd.print(plant);

  lcd.setCursor(0,1);
  lcd.print("Match:");
  lcd.print(score);
  lcd.print("%");
}



  delay(1000);
}
