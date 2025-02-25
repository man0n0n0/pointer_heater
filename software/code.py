import asyncio
import wifi
from adafruit_httpserver import Server, Request, JSONResponse, Response
import socketpool

from scripts.servo import random_movement
from scripts.thermal_display import get_temperatures, get_flat_pixels

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

@server.route("/temperatures")
def base(request: Request):
    flat_pixels = get_flat_pixels()
    return Response(request, str(flat_pixels))

#server.serve_forever(str(wifi.radio.ipv4_address))
server.serve_forever("192.168.4.1")

async def thermal_detection():
    while True:
        await get_temperatures()

async def servo_control(aimed_x_angle=None):
    while True:
        await random_movement(aimed_x_angle)


# define the main function to run the event loop
async def main():
    asyncio.create_task(thermal_detection())
    asyncio.create_task(servo_control())
    
# Create and run the event loop
loop = asyncio.get_event_loop()  
loop.create_task(main())  # Create a task to run the main function
loop.run_forever()  # Run the event loop indefinitely    
