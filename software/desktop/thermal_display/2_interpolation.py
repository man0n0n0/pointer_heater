import serial
import numpy as np
import pygame
from scipy.interpolate import griddata
from colour import Color
import math

# some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class ThermalCameraDisplay:
    def __init__(self, serial_port='/dev/tty.usbmodem2101'):
        # Initialize serial connection
        # self.ser = serial.Serial(serial_port)
        
        # Set temperature range (adjust based on your environment)
        self.min_temp = 20
        self.max_temp = 30
        
        # Set how many color values we can have
        self.colordepth = 1024
                
        # Display config
        self.height = 240
        self.width = 240
        self.displayPixelWidth = self.width / 30
        self.displayPixelHeight = self.height / 30
        # self.colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in list(Color("indigo").range_to(Color("red"), self.colordepth))]
        for c in list(Color("indigo").range_to(Color("red"), self.colordepth)): 
            self.colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255))]

        # Pygame config
        self.pygame = pygame
        self.lcd = None

        self.points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
        self.grid_x, self.grid_y = np.mgrid[0:7:32j, 0:7:32j]

    def pygame_start(self):
        self.pygame.init()
        self.lcd = self.pygame.display.set_mode((self.width, self.height))
        
        self.lcd.fill((255, 0, 0))

        self.pygame.display.update()
        self.pygame.mouse.set_visible(False)

        self.lcd.fill((0, 0, 0))
        self.pygame.display.update()

    def read_data(self):
        try:
            # Read serial line
            data = self.ser.readline().decode('utf-8').strip()
            
            # Convert to numpy array
            temps = np.array([float(x) for x in data.split(',')])
            return temps.reshape(8, 8)
        except:
            return None

    def update(self):
        pixels = []
        data = self.read_data()
        # for row in sensor.pixels:
        #     pixels = pixels + row
        # pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
        bicubic = griddata(self.points, pixels, (self.grid_x, self.grid_y), method="cubic")
        
        for ix, row in enumerate(bicubic):
            for jx, pixel in enumerate(row):
                self.pygame.draw.rect(
                    self.lcd,
                    self.colors[constrain(int(pixel), 0, COLORDEPTH - 1)],
                    (
                        self.displayPixelHeight * ix,
                        self.displayPixelWidth * jx,
                        self.displayPixelHeight,
                        self.displayPixelWidth,
                    ),
                )

        self.pygame.display.update()

    def run(self):
        self.update()
        
# Usage
if __name__ == '__main__':
    display = ThermalCameraDisplay('/dev/tty.usbmodem2101')  # Change port as needed
    display.pygame_start()
    display.run()
    