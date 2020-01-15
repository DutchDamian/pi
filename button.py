import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15,GPIO.OUT)
screenEnabled = True

def buttonCallback(channel):
  global screenEnabled
  if (screenEnabled):
    GPIO.output(15, GPIO.HIGH)
#    print("high")
  else:
#    print("low")
    GPIO.output(15, GPIO.LOW)
  screenEnabled = (not screenEnabled)


GPIO.add_event_detect(14,GPIO.FALLING,buttonCallback)

message = input("enter to quit")
GPIO.cleanup()
