#include <SoftwareSerial.h>
#include <Servo.h>

//Declaramos el servo
Servo servo_x;
Servo servo_y;

//Declaramos la variable
char dato;
int angulo = 90;

void setup() {

  //declaramos el periferico serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  //declaramos los pines de los servos X,Y 
  servo_x.attach(5);
  servo_y.attach(3);

  //inicializamos los servos a 90 grados 
  servo_x.write(angulo);
  servo_y.write(angulo);
}

void loop() {

  while(Serial.available()){
    dato = Serial.read();
    delay(10);
    Serial.println(dato);
    switch(dato){

      //Gira servo hacia la derecha
      case 'd':
      angulo=180;
      servo_x.write(angulo);
      break;
      
      //Gira servo hacia la izquierda
      case 'i':
      angulo=0;
      servo_x.write(angulo);
      break;
      
      

      //girar  hacia arriva
      case 'a':
      angulo=180;
      servo_y.write(angulo);
      break;

      //girar hacia abajo
      case 'b':
      angulo=0;
      servo_y.write(angulo);
      break;

      //Parar el servo
      case 'p':
      angulo=90;
      servo_x.write(angulo);
      servo_y.write(angulo);
      break;
      }
   }
 }