import RPi.GPIO as GPIO
import time
import math

class FunctionGenerator:
    def __init__(self, output_pin):
        self.output_pin = output_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.output_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.output_pin, 1000)  # Start PWM at 1000 Hz
        self.pwm.start(0)

    def square_wave(self, frequency):
        self.pwm.ChangeFrequency(frequency)
        self.pwm.ChangeDutyCycle(50)  # 50% duty cycle for square wave

    def sine_wave(self, frequency):
        # Approximation of sine wave using PWM
        for i in range(100):
            duty_cycle = 50 + 50 * math.sin(2 * math.pi * i / 100)
            self.pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(1 / (frequency * 100))

    def triangle_wave(self, frequency):
        # Approximation of triangle wave using PWM
        for i in range(100):
            if i < 50:
                duty_cycle = i * 2
            else:
                duty_cycle = 100 - (i - 50) * 2
            self.pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(1 / (frequency * 100))

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        fg = FunctionGenerator(18)  # Use GPIO 18
        while True:
            fg.square_wave(1)  # 1 Hz square wave
            time.sleep(5)
            fg.sine_wave(1)    # 1 Hz sine wave
            time.sleep(5)
            fg.triangle_wave(1)  # 1 Hz triangle wave
            time.sleep(5)
    except KeyboardInterrupt:
        fg.cleanup()