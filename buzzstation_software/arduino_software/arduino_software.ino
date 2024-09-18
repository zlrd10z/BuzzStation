#include "pins_arduino.h"
#include <SoftwareSerial.h>

#define LED_BUILTIN 13 
/* one note from pi have 3 bytes + 1 one byte for midi output information, so 250 notes can be send, last byte if for stop_byte - processing delimiter */
#define BUFFER_SIZE 1001 

unsigned char buffer[BUFFER_SIZE];
int buffer_position = 0;
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
  buffer_position = 0;

  while (Serial.available() > 0 && buffer_position < BUFFER_SIZE) {
    buffer[buffer_position++] = Serial.read();
    delay(1); // Small delay to allow buffer to fill
  }
  digitalWrite(LED_BUILTIN, LOW);
}

// Process data from the buffer, then route the data to MIDI output 2 or output 3
void processData() {
  int index = 0;
  while (index < buffer_position) {
    if (buffer[index] == stop_byte) {
      // Stop byte detected, end of message
      break;
    }
    if (buffer[index] == byte_midi_output_2) {
      if (index + 3 < buffer_position) {
        playNoteMIDI2(buffer[index + 1], buffer[index + 2], buffer[index + 3]);
        index += 4;
      } else {
        // Incomplete message
        break;
      }
    } else if (buffer[index] == byte_midi_output_3) {
      if (index + 3 < buffer_position) {
        playNoteMIDI3(buffer[index + 1], buffer[index + 2], buffer[index + 3]);
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
