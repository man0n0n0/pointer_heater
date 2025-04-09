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

