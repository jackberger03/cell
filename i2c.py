import board
import busio

def check_i2c_connection():
    """Checks if an I2C connection is working by trying to scan for devices."""

    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        devices = i2c.scan()

        if devices:
            print("I2C connection is working. Found devices:")
            for device_address in devices:
                print(f"  - 0x{device_address:02X}")
        else:
            print("I2C connection might not be working. No devices found.")

    except Exception as e:
        print(f"Error checking I2C connection: {e}")

if __name__ == "__main__":
    check_i2c_connection() 