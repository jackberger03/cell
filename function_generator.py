import time
import math
from adafruit_mcp4725 import MCP4725
import board

class FunctionGenerator:
    def __init__(self, dac):
        self.dac = dac
        self.running = True
        self.waveforms = ['square', 'triangle', 'sin']
        self.frequency = 1  # Default frequency
        self.max_voltage = 3.3  # Default max voltage

    def square_wave(self, duration):
        end_time = time.time() + duration
        period = 1 / self.frequency
        half_period = period / 2
        while time.time() < end_time:
            self.dac.voltage = self.max_voltage
            time.sleep(half_period)
            self.dac.voltage = 0
            time.sleep(half_period)

    def sine_wave(self, duration):
        end_time = time.time() + duration
        step = 0.01
        while time.time() < end_time:
            for t in range(int(1 / (self.frequency * step))):
                value = (math.sin(2 * math.pi * self.frequency * t * step) + 1) / 2
                self.dac.voltage = value * self.max_voltage
                time.sleep(step)

    def triangle_wave(self, duration):
        end_time = time.time() + duration
        step = 0.01
        while time.time() < end_time:
            for i in range(50):
                self.dac.voltage = (i / 50) * self.max_voltage
                time.sleep(step)
            for i in range(50, 0, -1):
                self.dac.voltage = (i / 50) * self.max_voltage
                time.sleep(step)

    def run(self):
        while self.running:
            for shape in self.waveforms:
                print(f"Generating {shape} wave")
                if shape == 'square':
                    self.square_wave(10)
                elif shape == 'triangle':
                    self.triangle_wave(10)
                elif shape == 'sin':
                    self.sine_wave(10)

if __name__ == "__main__":
    i2c = board.I2C()
    dac = MCP4725(i2c)
    fg = FunctionGenerator(dac)
    
    try:
        fg.run()
    except KeyboardInterrupt:
        print("\nStopping the function generator.")
        dac.voltage = 0  # Reset DAC output to 0V