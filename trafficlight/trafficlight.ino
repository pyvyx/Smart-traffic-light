#define CYCLE_TIME 10000 // in ms
#define RED_DELAY  500  // in ms

#define R1 2
#define G1 3
#define R2 4
#define G2 5
#define R3 6
#define G3 7
#define R4 8
#define G4 9

#define On(light) digitalWrite(light, HIGH)
#define Off(light) digitalWrite(light, LOW)

uint32_t prevTime = millis();
bool done = false;
bool Intersec1(bool forceSwitch = false)
{
  if(forceSwitch || (millis() - prevTime >= CYCLE_TIME && done))
  {
    Off(G2);
    Off(G4);
    On(R2);
    On(R4);
    // delay(RED_DELAY);
    
    Off(R1);
    Off(R3);
    On(G1);
    On(G3); 
    prevTime = millis();
    done = false;
    return true;
  }
  return false;
}


bool Intersec2(bool forceSwitch = false)
{
  if(forceSwitch || (millis() - prevTime >= CYCLE_TIME && !done))
  {
    Off(G1);
    Off(G3);
    On(R1);
    On(R3);
    //delay(RED_DELAY);

    Off(R2);
    Off(R4);
    On(G2);
    On(G4);
    prevTime = millis();
    done = true;
    return true;
  }  
  return false;
}


void setup() 
{  
  Serial.begin(9600);
  Intersec1(true);
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


void DefaultControl()
{
  Intersec1();
  Intersec2();
}

void loop() 
{
  while(!Serial.available())
    DefaultControl();

  // 0 - 1 - 0 - 0
  // 1 - 2 - 3 - 4
  String str = Serial.readString();
  int nums[4] = {0};
  nums[0] = str[0] - 48;
  nums[1] = str[1] - 48;
  nums[2] = str[2] - 48;
  nums[3] = str[3] - 48;

  if(nums[0] == 1 || nums[2] == 1)
  { 
    while(!Intersec1(true));
  }
  else if(nums[1] == 1 || nums[3] == 1)
  {
    while(!Intersec2(true));
  }
}