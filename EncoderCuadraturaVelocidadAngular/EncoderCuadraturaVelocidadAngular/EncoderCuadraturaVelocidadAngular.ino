/////////////////////////// COMUNICACION SERIAL //////////////////
String inputString = "";         
bool stringComplete = false;
const char separator = ',';
const int dataLength = 1;
double data[dataLength]; // Valor regula ciclo de trabajo (PWM)

unsigned long lastTime = 0, sampleTime = 100;  // Tiempo de muestreo

//////////////////////////// ENCONDER ///////////////////
const byte    C1 = 2; // Entrada de la señal A del encoder (Cable amarillo).
const byte    C2 = 3; // Entrada de la señal B del encoder (Cable verde).

////////////////////////// PUENTE H //////////////////////
const byte    in1 = 7;                  
const byte    in2 = 8;                  
const byte    enA = 6;                

volatile int count = 0;
volatile byte ant  = 0;
volatile byte act  = 0;

///////////////////// Variables Motor ////////////////

double w = 0.0;  // Velocidad angular en rad/s.
int outValue = 0; //Variable de control (pwm)
double constValue = 4.2; //(1000*2*pi)/R ---> R = 1980 Resolucion encoder cuadruple

void setup()
{
  /////////////////// CONFIGURACION PUERTO SERIAL ////////////////
  Serial.begin(115200);
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
     
    outValue=(int)data[0];

    inputString = "";
    stringComplete = false;
  }

  if (millis() - lastTime >= sampleTime)
  {      
      if (outValue > 0) anticlockwise(in2,in1,enA,outValue); else clockwise(in2,in1,enA,abs(outValue));     
      w =(constValue*count)/(millis()-lastTime); // Calculamos velocidad rad/s
      lastTime = millis(); // Almacenamos el tiempo actual.
      count = 0;  // Reiniciamos los pulsos.
      Serial.println(w);
      
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
