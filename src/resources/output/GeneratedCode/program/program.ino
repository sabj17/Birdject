#include <dht.h>
dht DHT;

#define pin1 1
#define pin2 2
#define pin3 3
#define pin4 4
#define pin5 5
#define pin6 6
#define pin7 7
#define pin8 8
#define pin9 9
#define pin10 10
#define pin11 11
#define pin12 12
#define pin13 13
#define pinA0 A0
#define pinA1 A1
#define pinA2 A2
#define pinA3 A3
#define pinA4 A4
#define pinA5 A5

// Not implemented
class List{
  public:
    void add(){}
    void remove(){}
    int size(){}
};

class Output {
  public:
    int pin;
    int state = 0;

    Output(int inputPin) {
      pin = inputPin;
    }
    void initialize() {
      pinMode(pin, OUTPUT);
    }

    bool setMode(bool newMode) {
      state = newMode;
      digitalWrite(pin, newMode);
      return newMode;
    }

    int isTurnedOn(){
      return state;
    }

    int changeMode() {
      if (state) {
        state = 0;
      } else {
        state = 1;
      }
      digitalWrite(pin, state);
      delay(200);
      return state;
    }
};

class Light : public Output {
  public:
    Light (int inputPin): Output(inputPin) {}
};

class Window : public Output {
  public:
    Window (int inputPin): Output(inputPin) {}

    int openTo(int degree){
        if(state != degree){
            state = degree;
            Serial.println(String("Window opened to ") + degree + String(" degrees"));
        }
        digitalWrite(pin, true);
        return state;
    }

    int close(){
        if(state > 0){
            state = 0;
            Serial.println("Window closed");
        }
        digitalWrite(pin, false);
        return state;
    }
};

class Radiator : public Output {
  public:
    Radiator (int inputPin): Output(inputPin) {}

    int getHeatLevel(){
        return Output::isTurnedOn();
    }

    void setHeatLevel(int level){
        if(0 <= level && level <= 5){
            state = level;
            Serial.println(String("New Heat Level Is: ") + level);
        }
    }

    int increase(){
      if(state < 5){
        state++;
      }
      Serial.println(String("Radiator value increased to: ") + state);
      digitalWrite(pin, state);
      delay(200);
      return state;
    }

    int decrease(){
      if(state > 0){
        state--;
      }
      Serial.println(String("Radiator value decreased to: ") + state);
      digitalWrite(pin, state);
      delay(200);
      return state;
    }
};

class Input {
  public:
    int pin;

    Input (int inputPin) {
      pin = inputPin;
    }

    void initialize() {
      pinMode(pin, INPUT);
    }

    int isTurnedOn() {
      return digitalRead(pin);
    }
};

class Switch : public Input {
  public:
    Switch (int inputPin): Input(inputPin) {}
};

class Thermometer : public Input {
  public:
    Thermometer (int inputPin): Input(inputPin) {}

    float isTurnedOn() {
      return analogRead(pin);
    }

    float getTemp(){
        DHT.read11(pin);
        delay(200);
        return DHT.temperature;
    }
};

// ///////////////// Generated Code Below ///////////////// //


class LivingRoomClass {
  public:
Light light;
Switch switch1;

LivingRoomClass() : light(pin8) , switch1(pin2) {}

} LivingRoom;



class KitchenClass {
  public:
Light light;
Switch switch;

KitchenClass() : light(pin9) , switch(pin3) {}

} Kitchen;

void initializeObjects(){
LivingRoom.light.initialize();
LivingRoom.switch1.initialize();
Kitchen.light.initialize();
Kitchen.switch.initialize();
}

void setup() {
Serial.begin(9600);
initializeObjects();
}

void loop() {

if (LivingRoom.switch1.isTurnedOn()){
LivingRoom.light.changeMode();
}

if (Kitchen.switch.isTurnedOn()){
Kitchen.light.changeMode();
}
}
