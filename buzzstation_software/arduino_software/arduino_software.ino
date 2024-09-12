#include "pins_arduino.h"
#include <SoftwareSerial.h>
#include <stdio.h>

#define LED_BUILTIN 13 
unsigned char buffor[1001];
int buffor_position;
unsigned char stop_byte = 224;
unsigned char byte_midi_output_2 = 222;
unsigned char byte_midi_output_3 = 223;

// Midi output 3:
SoftwareSerial softSerial(3,2); // Digital ports as 2 (RX) and 3 (TX)

void setup() {
  Serial.begin(31250); // 31250 baudrate - MIDI baudrate
  softSerial.begin(31250);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    if (Serial.available() > 0) {
      receiveData();
      processData();
    }
  }
}

// Receive data:
void receiveData(){
  digitalWrite(LED_BUILTIN, HIGH); // Indicate that data is transfered via Serial
  buffor_position = 0;

  while (Serial.available() > 0 && buffor_position < 1000) {
    buffor[buffor_position++] = Serial.read();  
  }
  buffor[buffor_position] = stop_byte;
  digitalWrite(LED_BUILTIN, LOW);
}

// Process data from the buffer, then route the data to MIDI output 2 or output 3
void processData(){
  buffor_position = 0;

  while (buffor[buffor_position] != stop_byte){
    if(buffor[buffor_position] == byte_midi_output_2){
      playNoteMIDI2(buffor[buffor_position + 1], buffor[buffor_position + 2], buffor[buffor_position + 3]);
      buffor_position += 4;
    }
    else if (buffor[buffor_position] == byte_midi_output_3){
      playNoteMIDI3(buffor[buffor_position + 1], buffor[buffor_position + 2], buffor[buffor_position + 3]);
      buffor_position += 4;
    }

    else{buffor_position++;}

  }

}

void playNoteMIDI2(int channel, int note, int velocity) {
  Serial.write(channel);
  Serial.write(note);
  Serial.write(velocity);
}

void playNoteMIDI3(int channel, int note, int velocity) {
  softSerial.write(channel);
  softSerial.write(note);
  softSerial.write(velocity);
}
