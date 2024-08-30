import time
import math
from adafruit_mcp4725 import MCP4725
import board

class FunctionGenerator:
    def __init__(self, dac):
        self.dac = dac
        self.running = True

    def square_wave(self, frequency, max_voltage, duration):
        end_time = time.time() + duration
        period = 1 / frequency
        half_period = period / 2
        while time.time() < end_time:
            self.dac.voltage = max_voltage
            time.sleep(half_period)
            self.dac.voltage = 0
            time.sleep(half_period)

    def sine_wave(self, frequency, max_voltage, duration):
        end_time = time.time() + duration
        step = 0.01
        while time.time() < end_time:
            for t in range(int(1 / (frequency * step))):
                value = (math.sin(2 * math.pi * frequency * t * step) + 1) / 2
                self.dac.voltage = value * max_voltage
                time.sleep(step)

    def triangle_wave(self, frequency, max_voltage, duration):
        end_time = time.time() + duration
        step = 0.01
        while time.time() < end_time:
            for i in range(50):
                self.dac.voltage = (i / 50) * max_voltage
                time.sleep(step)
            for i in range(50, 0, -1):
                self.dac.voltage = (i / 50) * max_voltage
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

        while True:
            try:
                duration = float(input("Enter duration in seconds: "))
                if duration > 0:
                    break
                print("Duration must be greater than 0. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        return shape, frequency, max_voltage, duration

    def run(self):
        while self.running:
            shape, frequency, max_voltage, duration = self.get_user_input()
            
            print(f"Generating {shape} wave at {frequency} Hz with {max_voltage}V max for {duration} seconds")
            if shape == 'square':
                print("Starting square wave generation...")
                self.square_wave(frequency, max_voltage, duration)
            elif shape == 'triangle':
                print("Starting triangle wave generation...")
                self.triangle_wave(frequency, max_voltage, duration)
            elif shape == 'sin':
                print("Starting sine wave generation...")
                self.sine_wave(frequency, max_voltage, duration)
            print("Wave generation complete.")
            
            choice = input("Generate another waveform? (y/n): ").lower()
            if choice != 'y':
                self.running = False

if __name__ == "__main__":
    i2c = board.I2C()
    dac = MCP4725(i2c)
    fg = FunctionGenerator(dac)
    
    try:
        fg.run()
    except KeyboardInterrupt:
        print("\nStopping the function generator.")
    finally:
        dac.voltage = 0  # Reset DAC output to 0V