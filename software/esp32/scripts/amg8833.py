import asyncio
import board
import adafruit_amg88xx
import busio

i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

def get_flat_pixels():
    # Read all 64 pixels
    pixels = amg.pixels
    
    # Flatten the 8x8 grid into a single sequence
    flat_pixels = [pixel for row in pixels for pixel in row]
    return flat_pixels

async def get_temperatures():
    flat_pixels = get_flat_pixels()
    
    # Send data over serial
    for i, temp in enumerate(flat_pixels):
        print(f"{temp:.1f}", end='')
        if i < len(flat_pixels)-1:
            print(',', end='')
    print()  # New line after each frame
    await asyncio.sleep(0.05)


