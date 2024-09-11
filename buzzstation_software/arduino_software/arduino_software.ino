#include "pins_arduino.h"
#include <SoftwareSerial.h>
#include <stdio.h>

unsigned char buffor [1000];
volatile byte position;
volatile boolean process_it;

// Special bytes:
unsigned char byte_spi_transsmision_stop = 120;
unsigned char byte_midi_output_2 = 121;
unsigned char byte_midi_output_3 = 122;

// Midi output 3:
SoftwareSerial softSerial(3,2); // Digital ports as 2 (RX) and 3 (TX)

void setup (void)
{
    // Midi output 2:
  Serial.begin(31250);
  softSerial.begin(31250);

  // have to send on master in, *slave out*
  pinMode(MISO, OUTPUT);
  
  // turn on SPI in slave mode
  SPCR |= _BV(SPE);
  
  // turn on interrupts
  SPCR |= _BV(SPIE);
  
  position = 0;
  process_it = false;
}  // end of setup


// SPI interrupt routine:
ISR (SPI_STC_vect)
{
byte c = SPDR;
  
  // add to bufforfer if room
  if (position < sizeof buffor)
    {
    buffor[position++] = c;
    // byte 120 means time to process bufforfer
    if (c == byte_spi_transsmision_stop)
      process_it = true;
      
    }  // end of room available
}

// main loop - wait for flag set in interrupt routine
void loop (void)
{
  if (process_it)
    {
    buffor[position] = 0;  

    // send buffor data to Serial and Software Serial:
    int x = 0;
    while (true){
      if (buffor[x] == byte_spi_transsmision_stop){
        break;
      }
      else if (buffor[x] == byte_midi_output_2){
        playNoteMIDI2(buffor[x + 1], buffor[x + 2], buffor[x + 3]);
        x += 4;
      }

      else if (buffor[x] == byte_midi_output_3){
        playNoteMIDI3(buffor[x + 1], buffor[x + 2], buffor[x + 3]);
        x += 4;
      }
      else {x += 1;
      }
      
    }

    position = 0;
    process_it = false;
    }  // end of flag set
    
}  // end of loop

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