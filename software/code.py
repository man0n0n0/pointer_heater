# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import busio
import board
import adafruit_amg88xx
import pwmio
from adafruit_motor import servo
import asyncio
import random

# create thermal detection objects
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

# create servo control involved object
pwmx = pwmio.PWMOut(board.IO20, frequency=50)
pwmy = pwmio.PWMOut(board.IO21, frequency=50)
servo_x = servo.ContinuousServo(pwmx)
servo_y = servo.ContinuousServo(pwmy)

async def thermal_detection():
    while True:
        # produce a thermal matrix
        for row in amg.pixels:
            # Pad to 1 decimal place
            print(["{0:.1f}".format(temp) for temp in row])
            print("")
        print("\n")
        time.sleep(1)

async def servo_control(aimed_x_angle=None):
    while True:
        x_angle = random(10,170) if not x_angle else aimed_x_angle
        
        if not prev_x_angle:
            prev_x_angle = 90 
            await asyncio.sleep(1)
            
        for angle in range(prev_x_angle, x_angle, 5):  # 0 - 180 degrees, 5 degrees at a time.
            servo_x.angle = angle
            time.sleep(0.05)
            
        prev_x_angle = x_angle

# define the main function to run the event loop
async def main():
    asyncio.create_task(thermal_detection())
    asyncio.create_task(servo_control())
    
# Create and run the event loop
loop = asyncio.get_event_loop()  
loop.create_task(main())  # Create a task to run the main function
loop.run_forever()  # Run the event loop indefinitely    


