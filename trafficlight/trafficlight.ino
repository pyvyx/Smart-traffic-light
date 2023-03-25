#define R1 2
#define G1 3
#define R2 4
#define G2 5
#define R3 6
#define G3 7
#define R4 8
#define G4 9

void setup() 
{  
  Serial.begin(9600);
  //for(char i = 0; i <= G4; ++i)
  //  pinMode(i, OUTPUT);
  
//  for (int i = 0 ; i < EEPROM.length() ; i++) {
//EEPROM.write(i, 0);
//}

  //Keyboard.begin();
}

void AllBlink()
{
  for(uint8_t i = R1; i <= G4; ++i)
  {
    if(i != 4 && i != 5 && i != 8 && i != 9)
      digitalWrite(i, HIGH);
  }
  digitalWrite(5, HIGH);
  digitalWrite(8, HIGH);

  digitalWrite(4, LOW);
  digitalWrite(9, LOW);
  
  delay(500);
  for(uint8_t i = R1; i <= G4; ++i)
  {
    if(i != 4 && i != 5 && i != 8 && i != 9)
      digitalWrite(i, LOW);
  }
  
  digitalWrite(5, LOW);
  digitalWrite(8, LOW);
  
  digitalWrite(4, HIGH);
  digitalWrite(9, HIGH);
  delay(500);
}

//void TestSingle()
//{
//  if (Serial.available() > 0) {
//
//    // read incoming serial data:
//
//    char inChar = Serial.read();
//
//    // Type the next ASCII value from what you received:
//
//    Keyboard.write(inChar);
//    Serial.println(inChar);
//  }
//}

void loop() 
{
  AllBlink();
}



