import time
import busio
import board
import adafruit_amg88xx
import pwmio
from adafruit_motor import servo
import asyncio
import random
import wifi
import ipaddress
from adafruit_httpserver import Server, Request, JSONResponse, Response
import socketpool
import microcontroller

# create thermal detection objects
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

# create servo control involved object
pwmx = pwmio.PWMOut(board.IO1, frequency=50)
pwmy = pwmio.PWMOut(board.IO2, frequency=50)
servo_x = servo.ContinuousServo(pwmx)
servo_y = servo.ContinuousServo(pwmy)

# Set access point on board
ssid = "broken_heart"
psw = "key_to_the_broken_heart"
wifi.radio.start_ap(ssid=ssid, password=psw)

# Configure websockets
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)
server.headers = {
    "Access-Control-Allow-Origin": "*",
}

def get_flat_pixels():
    pixels = amg.pixels
    
    # Flatten the 8x8 grid into a single sequence
    flat_pixels = [pixel for row in pixels for pixel in row]
    return flat_pixels

@server.route("/temperatures")
def base(request: Request):
    flat_pixels = get_flat_pixels()
    return Response(request, str(flat_pixels))

#server.serve_forever(str(wifi.radio.ipv4_address))
server.serve_forever("192.168.4.1")

async def thermal_detection():
    while True:
        # Read all 64 pixels
        pixels = amg.pixels
        
        # Flatten the 8x8 grid into a single sequence
        flat_pixels = [pixel for row in pixels for pixel in row]
        
        # Send data over serial
        for i, temp in enumerate(flat_pixels):
            print(f"{temp:.1f}", end='')
            if i < len(flat_pixels)-1:
                print(',', end='')
        print()  # New line after each frame
        await asyncio.sleep(0.05)


async def servo_control(aimed_x_angle=None):
    prev_x_angle = None
    while True:
        x_angle = random.randint(10,170) if not aimed_x_angle else aimed_x_angle
        print(f'new movement')
        if not prev_x_angle :
            prev_x_angle = 90 
            await asyncio.sleep(1)
            
        for angle in range(prev_x_angle, x_angle, 5):  # 0 - 180 degrees, 5 degrees at a time.
            servo_x.angle = angle
            print(f'moving to {angle}')
            await asyncio.sleep(0.05)
            
        prev_x_angle = x_angle

# define the main function to run the event loop
async def main():
    asyncio.create_task(thermal_detection())
    asyncio.create_task(servo_control())
    
# Create and run the event loop
loop = asyncio.get_event_loop()  
loop.create_task(main())  # Create a task to run the main function
loop.run_forever()  # Run the event loop indefinitely    
