#include "motorControl.h"

/////////////////////////// COMUNICACION SERIAL //////////////////
String inputString = "";         
bool stringComplete = false;
const char separator = ',';
const int dataLength = 1;
double data[dataLength]; // Velocidad de referencia (Sp) 

/////////////////////////// CONTROLADOR PID //////////////////
unsigned long lastTime = 0, sampleTime = 100;  // Tiempo de muestreo
motorControl motor(sampleTime);

//////////////////////////// ENCONDER ///////////////////
const byte    C1 = 3; // Entrada de la señal A del encoder (Cable amarillo).
const byte    C2 = 2; // Entrada de la señal B del encoder (Cable verde).

////////////////////////// PUENTE H //////////////////////
const byte    in1 = 7;                  
const byte    in2 = 8;                  
const byte    enA = 6;                

volatile int count = 0;
volatile byte ant  = 0;
volatile byte act  = 0;

///////////////////// Variables Motor ////////////////

double w = 0.0;     // Velocidad angular en rad/s.
double wRef = 0.0;  // Velocidad angular de referencia en rad/s.
int outValue = 0;   //Variable de control (pwm)
double constValue = 4.2; //(1000*2*pi)/R ---> R = 1496 Resolucion encoder cuadruple

void setup()
{
  /////////////////// CONFIGURACION PUERTO SERIAL ////////////////
  Serial.begin(115200);

  ////////////////// SINTONIA LAMBDA PID //////////////////
  
  motor.lambdaTunning(5.692,0.198,0.1437); // (K,tau,delay)
 
  Serial.print(motor.getK());
  Serial.print(", ");
  Serial.print(motor.getTi());
  Serial.print(", ");
  Serial.println(motor.getTd());

  ////////////////// SU PROPIA SINTONIA //////////////////
  
  //motor.setGains(0.07 , 0.27, 0.05); // (Kc,Ti,Td)
  
  ////////////////// Limites de señales //////////////////
  motor.setCvLimits(255,20); // Limites de Cv (0-255), considerar zona muerta
  motor.setPvLimits(11,0);   // Limites de Pv (rad/s)

  /////////////////// CONFIGURACION DE PINES ////////////////
  pinMode(C1, INPUT);
  pinMode(C2, INPUT);

  pinMode(in1, OUTPUT);       
  pinMode(in2, OUTPUT);   

  //////////////////// MOTOR APAGADO //////////////////////
  digitalWrite(in1, false);       
  digitalWrite(in2, false);   

  analogWrite(enA,outValue);

  ////////////////////////// INTERRUPCIONES /////////////////////
  attachInterrupt(digitalPinToInterrupt(C1), encoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(C2), encoder, CHANGE);
  
  lastTime = millis();
}

void loop() {
  
  ////////// SI RECIBE DATOS /////////////
  if (stringComplete) 
  {
    for (int i = 0; i < dataLength ; i++)
    {
      int index = inputString.indexOf(separator);
      data[i] = inputString.substring(0, index).toFloat();
      inputString = inputString.substring(index + 1);
     }
     
    wRef=data[0];

    inputString = "";
    stringComplete = false;
  }

  if (millis() - lastTime >= sampleTime)
  {
      w =(constValue*count)/(millis()-lastTime); // Calculamos velocidad rad/s
      lastTime = millis(); // Almacenamos el tiempo actual.
      count = 0;  // Reiniciamos los pulsos.
      outValue = motor.compute(wRef,w);  // Control PID    
      if (outValue > 0) anticlockwise(in2,in1,enA,outValue); else clockwise(in2,in1,enA,abs(outValue));     
      Serial.println(w);
     // Serial.println(outValue);
   } 

}


 
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
 
// Encoder precisión cuádruple.
void encoder(void)
{

    ant=act;                           
    act=PIND & 12;         
                           
    if(ant==0  && act== 4)  count++;
    if(ant==4  && act==12)  count++;
    if(ant==8  && act== 0)  count++;
    if(ant==12 && act== 8)  count++;
    
    if(ant==0 && act==8)  count--; 
    if(ant==4 && act==0)  count--;
    if(ant==8 && act==12) count--;
    if(ant==12 && act==4) count--;
    
}

void clockwise(int pin1, int pin2,int analogPin, int pwm)
{
  digitalWrite(pin1, LOW);  
  digitalWrite(pin2, HIGH);      
  analogWrite(analogPin,pwm);
}

void anticlockwise(int pin1, int pin2,int analogPin, int pwm)
{
  digitalWrite(pin1, HIGH);  
  digitalWrite(pin2, LOW);      
  analogWrite(analogPin,pwm);
}
