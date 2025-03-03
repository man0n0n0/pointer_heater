import adafruit_minimqtt.adafruit_minimqtt as MQTT
import wifi
import socketpool

SSID="SuperMango"
PWD="goodlife"
BROKER_IP="192.168.8.187"
MQTT_PORT = 1883

def new_mqtt_client():
    wifi.radio.connect(ssid=SSID, password=PWD)
    
    mqtt_client = MQTT.MQTT(
        broker=BROKER_IP,
        port=MQTT_PORT,
        socket_pool=socketpool.SocketPool(wifi.radio)
    )
    
    print("Connecting to MQTT broker...")
    mqtt_client.connect()
    print("Connected to MQTT broker!")

    return mqtt_client

