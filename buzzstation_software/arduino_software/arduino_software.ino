#include "pins_arduino.h"
#include <SoftwareSerial.h>

#define LED_BUILTIN 13 
/* one note from pi have 3 bytes + 1 one byte for midi output information, so 250 notes can be send, last byte if for stop_transsmision_byte - processing delimiter */
#define BUFFER_SIZE 1001 

unsigned char buffer[BUFFER_SIZE];
int buffer_position = 0;
unsigned char stop_transsmision_byte = 244;
unsigned char byte_midi_output_2 = 245;
unsigned char byte_midi_output_3 = 246;
unsigned char byte_all_notes_off = 247;
unsigned char singal_bytes_array[4] = {stop_transsmision_byte, 
                                       byte_midi_output_2, 
                                       byte_midi_output_3, 
                                       byte_all_notes_off
                                      };


SoftwareSerial softSerial(2, 3); // Digital ports as 2 (RX) and 3 (TX)

void setup() {
  Serial.begin(31250); // 31250 baudrate - MIDI baudrate
  softSerial.begin(31250);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    receive_data();
    process_data();
  }
}

// Receive data
void receive_data() {
  digitalWrite(LED_BUILTIN, HIGH); // Indicate that data is received via Serial
  buffer_position = 0;

  while (Serial.available() > 0 && buffer_position < BUFFER_SIZE) {
    buffer[buffer_position++] = Serial.read();
    delay(1); // Small delay to allow buffer to fill
  }
  digitalWrite(LED_BUILTIN, LOW);
}

// Process data from the buffer, then route the data to MIDI output 2 or output 3
void process_data() {
  int index = 0;
  bool send_two;
  bool send_three;
  while (index < buffer_position) {
    if (buffer[index] == stop_transsmision_byte) {
      // Stop byte detected, end of message
      break;
    }
    else if (buffer[index] == byte_all_notes_off){
      all_notes_off();
      index += 1;
    }

    //Check how long this single signal is:
    send_two = false;
    send_three = false;
    for (int i = 0; i < 4; i++){
      if (buffer[index+3] == singal_bytes_array[i]){
        send_two = true;
        break;
      }
      else if (buffer[index+4] == singal_bytes_array[i]){
        send_three = true;
        break;
      }
    }

   if (buffer[index] == byte_midi_output_2) {
      if(send_two){
        send_2bytes_output2(buffer[index + 1], buffer[index + 2]);
        index += 3;
      }
      else if (send_three){
        send_3bytes_output2(buffer[index + 1], buffer[index + 2], buffer[index + 3]);
        index += 4;
      } 
      else {
        // Incomplete message
        break;
      }
    } 
    else if (buffer[index] == byte_midi_output_3) {
      if(send_two){
        send_2bytes_output3(buffer[index + 1], buffer[index + 2]);
        index += 3;
      }
      else if (send_three){
        send_3bytes_output3(buffer[index + 1], buffer[index + 2], buffer[index + 3]);
        index += 4;
      } 
      else {
        // Incomplete message
        break;
      }
    }  
    else {
      index++;
      //transsmision / proccessing error, try to proceed to next index in order to recover
    }
  }
}

void send_3bytes_output2(int channel, int note, int velocity) {
  Serial.write(channel);
  Serial.write(note);
  Serial.write(velocity);
}

void send_3bytes_output3(int channel, int note, int velocity) {
  softSerial.write(channel);
  softSerial.write(note);
  softSerial.write(velocity);
}

void send_2bytes_output2(int channel, int value) {
  Serial.write(channel);
  Serial.write(value);
}

void send_2bytes_output3(int channel, int value) {
  softSerial.write(channel);
  softSerial.write(value);
}

// Send note off signal to all channels on both midi outputs:
void all_notes_off(){
  unsigned char note_off_byte = 123;
  unsigned char control_byte = 0;
  int channel;
  for(int i = 1; i < 17; i++){
    channel = 175;
    channel += i;
    unsigned char channel_byte = (unsigned char) channel;

    Serial.write(channel_byte);
    Serial.write(note_off_byte);
    Serial.write(control_byte);

    softSerial.write(channel_byte);
    softSerial.write(note_off_byte);
    softSerial.write(control_byte);
  }

}
