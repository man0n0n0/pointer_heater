import random
import asyncio
import pwmio
from adafruit_motor import servo

class Servo:
    def __init__(self, gpio):
        self.pwm = pwmio.PWMOut(gpio, frequency=50)
        self.servo = servo.Servo(self.pwm)
        self.prev_angle = 90
    
    async def move_to_angle(self, angle):
        increment = 5 if self.prev_angle < angle else -5
        for a in range(self.prev_angle,angle,increment):
            self.servo.angle = int(a)
            await asyncio.sleep(0.2)
        self.prev_angle = angle

    

        
"""
# I split this method in two (see below)
# To allow better integration with the mqtt workflow
# But obviously feel free to change this or revert it back to its previous state :))
# The only thing is that we should avoid printing stuff and instead send the data on the mqtt broker

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

"""