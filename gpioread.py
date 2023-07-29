#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

# Pin Definitions
input_pin = 18  # BCM pin 18, BOARD pin 12

def main():
    prev_value = None

    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setup(input_pin, GPIO.IN)  # set pin as an input pin
    print("Starting demo now! Press CTRL+C to exit")
    highs = 0
    try:
        for a in range(100):
            value_str = "LOW"
            value = GPIO.input(input_pin)
            if value == GPIO.HIGH:
                value_str = "HIGH"
                highs = highs + 1
            else: 
                value_str = "LOW"
            print("Value read from pin {} : {}".format(input_pin,
                                                           value_str))
            time.sleep(0.01)
    finally:
        print(highs)
        GPIO.cleanup()

if __name__ == '__main__':
    main()
