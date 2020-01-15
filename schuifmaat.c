#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <wiringPi.h>

#define REQ_PIN 34
#define CLK_PIN 32
#define DATA_PIN 33

int buffer[52];

void setup()
{
    wiringPiSetupGpio();
    pinMode(REQ_PIN, OUTPUT);
    pinMode(CLK_PIN, INPUT);
    pinMode(DATA_PIN, INPUT);
    digitalWrite(REQ_PIN, HIGH);
}

void collectData()
{
    int i = 0;
    int clk = 0;
    int data = 0;
    int prevClk = 1;

    digitalWrite(REQ_PIN, LOW);

    while(1)
    {
        data = digitalRead(DATA_PIN);
        clk = digitalRead(CLK_PIN);
//	printf("%d",clk);
        if(!clk && prevClk) {

           buffer[i] = data;
           i++;

           if(i == 52)
           {
                digitalWrite(REQ_PIN, LOW);
                break;
            }
        }

        prevClk = clk;
    }
}

void validateData()
{
    int isValid = 1;
    int i = 0;

    for(i = 0; i < 52; i++)
    {
        //first 16 bits not 1 -> wrong data type
        //last four not 0 -> unit not in mm - 36 35 34 33

        if(i < 16 & buffer[i] != 1 || i >= 48 && buffer[i] != 0) {
           collectData();
           validateData();
        }
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

    convert_num(&digits[0], 20);
    convert_num(&digits[1], 24);
    convert_num(&digits[2], 28);
    convert_num(&digits[3], 32);
    convert_num(&digits[4], 36);
    convert_num(&digits[5], 40);

    num = (digits[0] * 100000) + (digits[1]* 10000) + (digits[2] * 1000)
          + (digits[3] * 100) + (digits[4] * 10) + digits[5];
    float f_num = (float)num;

    //TODO: make dynamic
    return f_num / 1000.0;
}

//int main()
float meassureDistance()
{
    setup();
    collectData();
    validateData();
    return convertSignalToDecimal();
//    printf("%d",convertSignalToDecimal());
//    return 0;
}
