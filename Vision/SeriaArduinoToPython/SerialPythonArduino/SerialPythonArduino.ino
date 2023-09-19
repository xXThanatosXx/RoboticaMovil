unsigned long lastTime,sampleTime; // Tiempo muestreo 

String inputString = "";  // Almacenar la cadena recibida   
bool stringComplete = false;// Indicar que ha recibido una cadena
const char separator = ','; // Separador (,)
const int dataLength = 2; // Cantidad de datos que vamos recibir
double data[dataLength]; // Vector que va almacenar los datos recibidos

void setup() {

 Serial.begin(115200); // Configurar los baudios para la comunicación con el módulo Bluetooth

  
  sampleTime = 100; // Tiempo de muestreo 100ms
  lastTime = millis(); // Tiempo transcurrido
}

void loop() {
  
  if (stringComplete) 
  {
    for (int i = 0; i < dataLength ; i++)
    {
      int index = inputString.indexOf(separator);
      data[i] = inputString.substring(0, index).toFloat();
      inputString = inputString.substring(index + 1);
    }
    inputString = "";
    stringComplete = false;
  }


 if (millis()-lastTime >= sampleTime)
 {
  lastTime=millis();
   Serial.println(data[0],3);
   Serial.println(data[1],3);
 }

}

void serialEvent() {
  while ( Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
