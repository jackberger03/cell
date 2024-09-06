import time
import math
import adafruit_mcp4725
import busio
import board
import RPi.GPIO as GPIO

class FunctionGenerator:
    def __init__(self, dac, button_pin):
        self.dac = dac
        self.running = False
        self.button_pin = button_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self.toggle_running, bouncetime=200)

    def toggle_running(self, channel):
        self.running = not self.running

    def scale_voltage(self, value, max_voltage):
        return int((value / 3.3) * 4095 * (max_voltage / 3.3))

    def square_wave(self, frequency, max_voltage, duration):
        end_time = time.time() + duration
        period = 1 / frequency
        half_period = period / 2
        while time.time() < end_time and self.running:
            self.dac.raw_value = self.scale_voltage(max_voltage, max_voltage)
            time.sleep(half_period)
            self.dac.raw_value = 0
            time.sleep(half_period)

    def sine_wave(self, frequency, max_voltage, duration):
        end_time = time.time() + duration
        step = 0.001
        while time.time() < end_time and self.running:
            for t in range(int(1 / (frequency * step))):
                if not self.running:
                    break
                value = (math.sin(2 * math.pi * frequency * t * step) + 1) / 2
                self.dac.raw_value = self.scale_voltage(value * max_voltage, max_voltage)
                time.sleep(step)

    def triangle_wave(self, frequency, max_voltage, duration):
        end_time = time.time() + duration
        step = 1 / (frequency * 100)
        while time.time() < end_time and self.running:
            for i in range(100):
                if not self.running:
                    break
                self.dac.raw_value = self.scale_voltage((i / 100) * max_voltage, max_voltage)
                time.sleep(step)
            for i in range(100, 0, -1):
                if not self.running:
                    break
                self.dac.raw_value = self.scale_voltage((i / 100) * max_voltage, max_voltage)
                time.sleep(step)

    def get_user_input(self):
        while True:
            shape = input("Enter waveform shape (square, triangle, or sin): ").lower()
            if shape in ['square', 'triangle', 'sin']:
                break
            print("Invalid shape. Please try again.")

        while True:
            try:
                frequency = float(input("Enter frequency (up to 50 Hz): "))
                if 0 < frequency <= 50:
                    break
                print("Frequency must be between 0 and 50 Hz. Please try again.")
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

    def run(self):
        print("Press the button to start/stop wave generation.")
        while True:
            if self.running:
                shape, frequency, max_voltage = self.get_user_input()
                print(f"Generating {shape} wave at {frequency} Hz with {max_voltage}V max")
                if shape == 'square':
                    self.square_wave(frequency, max_voltage, float('inf'))
                elif shape == 'triangle':
                    self.triangle_wave(frequency, max_voltage, float('inf'))
                elif shape == 'sin':
                    self.sine_wave(frequency, max_voltage, float('inf'))
                self.dac.raw_value = 0
                print("Wave generation stopped.")
            else:
                time.sleep(0.1)

if __name__ == "__main__":
    i2c = busio.I2C(board.SCL, board.SDA)
    dac = adafruit_mcp4725.MCP4725(i2c)
    button_pin = 17  # Change this to the GPIO pin you're using for the button
    fg = FunctionGenerator(dac, button_pin)
    
    try:
        fg.run()
    except KeyboardInterrupt:
        print("\nStopping the function generator.")
    finally:
        dac.raw_value = 0  # Reset DAC output to 0V
        GPIO.cleanup()