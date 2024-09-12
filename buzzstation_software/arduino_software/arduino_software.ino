#include "pins_arduino.h"
#include <SoftwareSerial.h>

#define LED_BUILTIN 13 
#define BUFFER_SIZE 1000

unsigned char buffor[BUFFER_SIZE];
int buffor_position = 0;
unsigned char stop_byte = 221;
unsigned char byte_midi_output_2 = 222;
unsigned char byte_midi_output_3 = 223;

SoftwareSerial softSerial(3, 2); // Digital ports as 2 (RX) and 3 (TX)

void setup() {
  Serial.begin(31250); // 31250 baudrate - MIDI baudrate
  softSerial.begin(31250);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    receiveData();
    processData();
  }
}

// Receive data
void receiveData() {
  digitalWrite(LED_BUILTIN, HIGH); // Indicate that data is transferred via Serial
  buffor_position = 0;

  while (Serial.available() > 0 && buffor_position < BUFFER_SIZE) {
    buffor[buffor_position++] = Serial.read();
    delay(1); // Small delay to allow buffer to fill
  }
  digitalWrite(LED_BUILTIN, LOW);
}

// Process data from the buffer, then route the data to MIDI output 2 or output 3
void processData() {
  int index = 0;
  while (index < buffor_position) {
    if (buffor[index] == stop_byte) {
      // Stop byte detected, end of message
      break;
    }
    if (buffor[index] == byte_midi_output_2) {
      if (index + 3 < buffor_position) {
        playNoteMIDI2(buffor[index + 1], buffor[index + 2], buffor[index + 3]);
        index += 4;
      } else {
        // Incomplete message
        break;
      }
    } else if (buffor[index] == byte_midi_output_3) {
      if (index + 3 < buffor_position) {
        playNoteMIDI3(buffor[index + 1], buffor[index + 2], buffor[index + 3]);
        index += 4;
      } else {
        // Incomplete message
        break;
      }
    } else {
      index++;
    }
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
