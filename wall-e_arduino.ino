#include <Servo.h>
Servo myservo1;
Servo myservo2;

byte rx = 0; // variabile per contenere il carattere ricevuto. 
int pan = 90;
int tilt = 77;

void setup()
  {
Serial.begin(115200); // imposto la seriale per lavorare a 115200 baud
myservo1.attach(6);
myservo1.write(pan);
myservo2.attach(5);
myservo2.write(tilt);
Serial.flush(); // svuoto il buffer di ricezione seriale.
delay(100);
  }

void loop()
  {

  if (Serial.available() >0) // Controllo se il buffer di ricezione contiene qualcosa
    {
      rx = Serial.read(); // leggo il carattere ricevuto e lo memorizzo in rx
      Serial.flush(); // svuoto il buffer di ricezione seriale
      if (rx != '0')
       {
        if (rx=='1')
          {
            if (pan >= 35)
            {
              pan = pan - 2;
            }
          }
        if (rx=='2')
          {
            if (pan <= 135)
            {
              pan = pan + 2;
            }
          } 
        if (rx=='3')
          {
            if (tilt >= 35)
            {
              tilt = tilt - 2;
            }
          }
        if (rx=='4')
          {
            if (tilt <= 125)
            {
              tilt = tilt + 2;
            }
          }
       } 
        myservo1.write(pan);
        myservo2.write(tilt);
  }  }  
