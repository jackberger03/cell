import time
import math
import adafruit_mcp4725
import busio
import board
import RPi.GPIO as GPIO

class FunctionGenerator:
    # initializes the i2c bus, dac, and button pin
    def __init__(self, dac, button_pin):
        self.dac = dac
        self.running = False
        self.button_pin = button_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.last_button_state = GPIO.input(self.button_pin)

    # checks if the button is pressed
    def check_button(self):
        button_state = GPIO.input(self.button_pin)
        if button_state != self.last_button_state:
            self.last_button_state = button_state
            if button_state == GPIO.LOW:
                self.running = not self.running
                return True
        return False

    # converts the voltage I want into something the dac can read
    def scale_voltage(self, value, max_voltage):
        return int((value / 3.3) * 4095 * (max_voltage / 3.3))

    def square_wave(self, frequency, max_voltage):
        # calculates the period and half period
        period = 1 / frequency
        half_period = period / 2
        while self.running:
            # checks if the button is pressed
            if self.check_button():
                break
            # sets the dac to the max voltage
            self.dac.raw_value = self.scale_voltage(max_voltage, max_voltage)
            time.sleep(half_period)
            # checks if the button is pressed
            if self.check_button():
                break
            # sets the dac to 0
            self.dac.raw_value = 0
            time.sleep(half_period)

    def sine_wave(self, frequency, max_voltage):
        # sets the step size
        step = 0.001
        while self.running:
            # calculates the number of steps in a period and creates a for loop for one sin cycle or 2pi
            # basically this simplifies making sin wave by reducing each iteration to one period
            for t in range(int(1 / (frequency * step))):
                # checks if the button is pressed
                if self.check_button():
                    return
                # calculates the value of the sine wave at the current step
                value = (math.sin(2 * math.pi * frequency * t * step) + 1) / 2
                # sets the dac to the value of the sine wave
                self.dac.raw_value = self.scale_voltage(value * max_voltage, max_voltage)
                time.sleep(step)

    def triangle_wave(self, frequency, max_voltage):
        # sets the step size
        step = 1 / (frequency * 100)
        while self.running:
            # creates a for loop for one triangle wave cycle
            for i in range(100):
                # checks if the button is pressed
                if self.check_button():
                    return
                # sets the voltage to continuosly increase for 100 steps on the first half of the triangle wave
                self.dac.raw_value = self.scale_voltage((i / 100) * max_voltage, max_voltage)
                time.sleep(step)
            # creates a for loop for the other half of the triangle wave
            for i in range(100, 0, -1):
                # checks if the button is pressed
                if self.check_button():
                    return
                # sets the voltage to continuosly decrease for 100 steps on the second half of the triangle wave
                self.dac.raw_value = self.scale_voltage((i / 100) * max_voltage, max_voltage)
                time.sleep(step)

    # just a general chat interface for whenver the user hits the button
    # pretty simple but I did add error checking
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
            if self.check_button() and self.running:
                shape, frequency, max_voltage = self.get_user_input()
                print(f"Generating {shape} wave at {frequency} Hz with {max_voltage}V max")
                if shape == 'square':
                    self.square_wave(frequency, max_voltage)
                elif shape == 'triangle':
                    self.triangle_wave(frequency, max_voltage)
                elif shape == 'sin':
                    self.sine_wave(frequency, max_voltage)
                self.dac.raw_value = 0
                print("Wave generation stopped.")
            time.sleep(0.01)

# main function that initializes i2c, the dac, and button and then also has a keyboard interrupt with a gpio cleanup call so you can stop the program safely
if __name__ == "__main__":

    i2c = busio.I2C(board.SCL, board.SDA)
    dac = adafruit_mcp4725.MCP4725(i2c)
    # button pin is 17
    button_pin = 17
    # sets the function generator to fg
    fg = FunctionGenerator(dac, button_pin)

    # try and except for keyboard interrupt so you can stop the program safely
    try:
        fg.run()
    except KeyboardInterrupt:
        print("\nStopping the function generator.")
    finally:
        dac.raw_value = 0
        GPIO.cleanup()