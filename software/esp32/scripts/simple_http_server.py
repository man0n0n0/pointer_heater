from adafruit_httpserver import Server, Request, Response, Websocket, GET, mime_types as MIMEType, JSONResponse
import socketpool
import wifi
import os

ESP32_IP_ADDRESS = "192.168.4.1"
ESP32_SSID = "broken_heart"
ESP32_PWD = "key_to_the_broken_heart"

WIFI_SSID = "TADAAM_QD2603N"
WIFI_PWD = "AJN7DBM4GN55"

# Connect to wifi
wifi.radio.connect(ssid=WIFI_SSID,password=WIFI_PWD)

# Set access point on board
wifi.radio.start_ap(ssid=ESP32_SSID, password=ESP32_PWD)

# Server basic config
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)
server.headers = {
    "Access-Control-Allow-Origin": "*",
}

# Routes
@server.route("/")
def base(request: Request):
    return JSONResponse(request, {"what": "heyyy"})

# Run server
server.serve_forever(ESP32_IP_ADDRESS)
