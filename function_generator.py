import RPi.GPIO as GPIO
import time
import math
from adafruit_mcp4725 import MCP4725
import board

class FunctionGenerator:
    def __init__(self, dac, button_pin):
        self.dac = dac
        self.button_pin = button_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self.button_callback, bouncetime=200)
        self.running = False

    def square_wave(self, frequency, max_voltage):
        period = 1 / frequency
        half_period = period / 2
        while self.running:
            self.dac.normalized_value = 1.0  # High
            time.sleep(half_period)
            self.dac.normalized_value = 0.0  # Low
            time.sleep(half_period)

    def sine_wave(self, frequency, max_voltage):
        period = 1 / frequency
        step = 0.01  # Adjust for smoother/coarser wave
        while self.running:
            for t in range(int(period / step)):
                if not self.running:
                    break
                value = (math.sin(2 * math.pi * frequency * t * step) + 1) / 2
                self.dac.normalized_value = value
                time.sleep(step)

    def triangle_wave(self, frequency, max_voltage):
        period = 1 / frequency
        step = 0.01  # Adjust for smoother/coarser wave
        while self.running:
            # Rising edge
            for i in range(50):
                if not self.running:
                    break
                self.dac.normalized_value = i / 50
                time.sleep(step)
            # Falling edge
            for i in range(50, 0, -1):
                if not self.running:
                    break
                self.dac.normalized_value = i / 50
                time.sleep(step)

    def get_user_input(self):
        while True:
            shape = input("Enter waveform shape (square, triangle, or sin): ").lower()
            if shape in ['square', 'triangle', 'sin']:
                break
            print("Invalid shape. Please try again.")

        while True:
            try:
                frequency = float(input("Enter frequency (up to 20 Hz): "))
                if 0 < frequency <= 20:
                    break
                print("Frequency must be between 0 and 20 Hz. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            try:
                max_voltage = float(input("Enter maximum output voltage (0-3.3V): "))
                if 0 <= max_voltage <= 3.3:
                    break
                print("Voltage must be between 0 and 3.3V. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        return shape, frequency, max_voltage

    def button_callback(self, channel):
        self.running = not self.running

    def run(self):
        while True:
            if self.running:
                shape, frequency, max_voltage = self.get_user_input()
                
                while self.running:
                    if shape == 'square':
                        self.square_wave(frequency, max_voltage)
                    elif shape == 'triangle':
                        self.triangle_wave(frequency, max_voltage)
                    elif shape == 'sin':
                        self.sine_wave(frequency, max_voltage)
            else:
                time.sleep(0.1)  # Small delay to prevent CPU hogging

if __name__ == "__main__":
    i2c = board.I2C()
    dac = MCP4725(i2c)
    button_pin = 21
    fg = FunctionGenerator(dac, button_pin)
    
    try:
        fg.run()
    except KeyboardInterrupt:
        GPIO.cleanup()