import time
import math
import board
import busio
import adafruit_mcp4725

def sin_wave():
    i2c = busio.I2C(board.SCL, board.SDA)
    dac = adafruit_mcp4725.MCP4725(i2c)

    t = 0.0
    tStep = 0.05

    while True:
        voltage = 2048 * (1.0 + 0.5 * math.sin(6.2832 * t))
        dac.raw_value = int(voltage)
        t += tStep
        time.sleep(0.0005)

if __name__ == "__main__":
    try:
        sin_wave()
    except KeyboardInterrupt:
        print("Stopped by user")