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
        print(f"Generating square wave on pin {pin} at {frequency} Hz")
        print(f"Period: {period:.6f} seconds")
        print("Press Ctrl+C to stop")

if __name__ == "__main__":
    try:
        square_wave(18, 100000)  # 100 kHz on GPIO 18
    except KeyboardInterrupt:
        GPIO.cleanup()