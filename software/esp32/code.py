from asyncio import create_task, gather, run, sleep as async_sleep
import asyncio
import json

from scripts.servo import Servo
from scripts.amg8833 import get_flat_pixels
from scripts.mqtt import new_mqtt_client

mqtt_client = new_mqtt_client()
servo_client = Servo()

async def thermal_detection():
    while True:
        data = {"matrix": get_flat_pixels()}
        mqtt_client.publish("temperatures", json.dumps(data))
        await asyncio.sleep(0.1)


async def servo_control():
    while True:
        mqtt_client.publish("movement", json.dumps({"angle": "new movement"}))
        await asyncio.sleep(1)
       
        angles = await servo_client.get_random_angles_range()
        for angle in angles:
            await servo_client.move_to_x_angle(angle)
            mqtt_client.publish("movement", json.dumps({"angle": angle}))
            await asyncio.sleep(0.05)


# define the main function to run the event loop
async def main():
    asyncio.create_task(thermal_detection())
    asyncio.create_task(servo_control())

# Create and run the event loop
loop = asyncio.get_event_loop()  
loop.create_task(main())  # Create a task to run the main function
loop.run_forever()  # Run the event loop indefinitely

