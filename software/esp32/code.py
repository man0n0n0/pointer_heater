from asyncio import create_task, gather, run, sleep as async_sleep
import asyncio
import json
import random
import board

from scripts.servo import Servo
from scripts.amg8833 import get_flat_pixels
from scripts.mqtt import new_mqtt_client

mqtt_client = new_mqtt_client()
servo_x = Servo(board.IO5)
servo_y = Servo(board.IO6)
data = {}

async def thermal_detection():
    global data
    while True:
        data = {"matrix": get_flat_pixels()}
        mqtt_client.publish("temperatures", json.dumps(data))
        await asyncio.sleep(0.1)

async def servo_x_control():
    while True:
        '''back and forward of the moving range'''
        for angle in range(10,170) : 
            await servo_x.move_to_angle(angle)
            # mqtt_client.publish("angle_x", json.dumps(angles['x']))
            await asyncio.sleep(0.05)
        for angle in range(170,10, -1) : 
            await servo_x.move_to_angle(angle)
            # mqtt_client.publish("angle_x", json.dumps(angles['x']))
            await asyncio.sleep(0.05)           

async def servo_y_control():
    angle = 90
    while True:
        '''move toward the heat source'''
        y_direction = 1 if max(data["matrix"]) > 32 else -1 # as it is the middle of 64 point flattenend
        angle += y_direction
        angle = min(max(angle,80),110) # physical limit (80,110)
        await servo_y.move_to_angle(angle)
        #mqtt_client.publish("angle_y", json.dumps(angles['y']))
        await asyncio.sleep(0.05)

# define the main function to run the event loop
async def main():
    asyncio.create_task(thermal_detection())
    asyncio.create_task(servo_x_control())
    asyncio.create_task(servo_y_control())

# Create and run the event loop
loop = asyncio.get_event_loop()  
loop.create_task(main())  # Create a task to run the main function
loop.run_forever()  # Run the event loop indefinitely

