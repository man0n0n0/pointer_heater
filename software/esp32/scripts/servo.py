import random
import asyncio
import board
import pwmio
from adafruit_motor import servo

# create servo control involved object
pwmx = pwmio.PWMOut(board.IO1, frequency=50)
pwmy = pwmio.PWMOut(board.IO2, frequency=50)
servo_x = servo.Servo(pwmx)
servo_y = servo.Servo(pwmy)

async def random_movement(aimed_x_angle=None):
    try:
        prev_x_angle
    except NameError: 
        prev_x_angle = None

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
