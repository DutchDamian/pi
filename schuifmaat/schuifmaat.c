#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <wiringPi.h>

#define REQ_PIN 0
#define CLK_PIN 2
#define DATA_PIN 3

int buffer[37];

void setup()
{
    wiringPiSetup();
    pinMode(REQ_PIN, OUTPUT);
    pinMode(CLK_PIN, INPUT);
    pinMode(DATA_PIN, INPUT);
    digitalWrite(REQ_PIN, HIGH);
}

void collectData()
{
    int i, clk, data = 0;
    int prevClk = 1;

    digitalWrite(REQ_PIN, LOW);

    while(1)
    {
        clk = digitalRead(CLK_PIN);
        data = digitalRead(DATA_PIN);

        if(!clk && prevClk) {
            if(data)
            {
                i++;
                if(i == 16)
                {
                    i = 0;
                    prevClk = 1;
                    break;
                }
            } else {
                i = 0;
            }
        }

        prevClk = clk;
    }

    while(1)
    {
        clk = digitalRead(CLK_PIN);
        data = digitalRead(DATA_PIN);

        if(!clk && prevClk) {
            buffer[i] = data;
            i++;

            if(i == 36)
            {
		digitalWrite(REQ_PIN, HIGH);
                break;
            }
        }

        prevClk = clk;
    }
}

void validateData()
{
    //first bit not a 1 -> wrong data type
    //last four not 0 -> unit not in mm - 36 35 34 33
    //if first digit from numerical data isn't 0 it's probably wrong
    if(buffer[0] != 1 || buffer[33] != 0 || buffer[34] != 0 || buffer[35] != 0 || buffer[36] != 0
      || buffer[5] != 0 || buffer[6] != 0 || buffer[7] != 0 || buffer[8] != 0)
    {
        int i = 0;
        for(i = 0; i < 37; i++)
        {
            buffer[i] = 0;
        }

        collectData();
        validateData();
    }
}

int *convert_num(int *result, int start)
{
  //initializing these in one line causes some variables to not to be set to 0
  unsigned int i = 0;
  unsigned int num_i = 0;
  unsigned int num = 0;

  for(i = start; i < start + 4; i++)
  {
    	unsigned int temp = 0;
        temp =  buffer[i] << num_i;
    	num = num + temp;
   	num_i++;
  }

  *result = num;

  return result;
}

float convertSignalToDecimal()
{
   int num = 0;

   int digits[6] = {0};

    convert_num(&digits[0], 5);
    convert_num(&digits[1], 9);
    convert_num(&digits[2], 13);
    convert_num(&digits[3], 17);
    convert_num(&digits[4], 21);
    convert_num(&digits[5], 25);

    num = (digits[0] * 100000) + (digits[1]* 10000) + (digits[2] * 1000)
          + (digits[3] * 100) + (digits[4] * 10) + digits[5];
    float f_num = (float)num;

    //TODO: make dynamic
    return f_num / 1000.0;
}

float meassureDistance()
{
    setup();
    collectData();
    validateData();
    return convertSignalToDecimal();
}
