import asyncio
import board
import adafruit_amg88xx
import busio

print(board.SCL, board.SDA)

i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

def get_flat_pixels():
    # Read all 64 pixels
    pixels = amg.pixels
    
    # Flatten the 8x8 grid into a single sequence
    flat_pixels = [pixel for row in pixels for pixel in row]
    return flat_pixels



