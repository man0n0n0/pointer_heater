import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ThermalCameraDisplay:
    def __init__(self, serial_port='/dev/tty.usbmodem2101'):
        # Initialize serial connection
        self.ser = serial.Serial(serial_port)
        
        # Set up the plot
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.img = None
        
        # Set temperature range (adjust based on your environment)
        self.min_temp = 12
        self.max_temp = 30
        
    def read_data(self):
        try:
            # Read serial line
            data = self.ser.readline().decode('utf-8').strip()
            
            # Convert to numpy array
            temps = np.array([float(x) for x in data.split(',')])
            return temps.reshape(8, 8)
        except:
            return None
    
    def update(self, frame):
        # Read new data
        data = self.read_data()
        
        # Update plot if we got valid data
        if data is not None:
            if self.img is None:
                self.img = self.ax.imshow(data, cmap='hot',
                                        interpolation='nearest',
                                        vmin=self.min_temp,
                                        vmax=self.max_temp)
                
                plt.colorbar(self.img)
                self.ax.set_title('Thermal Camera View')
            else:
                self.img.set_array(data)
        
        return self.img,

    def run(self):
        ani = FuncAnimation(self.fig, self.update, interval=100,
                          blit=True)
        plt.show()

# Usage
if __name__ == '__main__':
    display = ThermalCameraDisplay('')  # Change port as needed
    display.run()