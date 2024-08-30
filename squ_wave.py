import RPi.GPIO as GPIO
import time

def square_wave(pin, frequency):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    period = 1.0 / frequency
    while True:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(period / 2)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(period / 2)

if __name__ == "__main__":
    try:
        square_wave(24, 1000)  # 100 kHz on GPIO 18
    except KeyboardInterrupt:
        GPIO.cleanup()