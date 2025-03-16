import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    print(f"Connected with result code {rc}")
    client.subscribe("test/topic")  # Replace with your desired topic

def on_message(client, userdata, msg):
    """Callback when message arrives"""
    print(f"Topic: {msg.topic}")
    print(f"Message: {msg.payload.decode()}")

# Create MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

try:
    # Connect to broker (replace localhost with actual broker address if needed)
    client.connect("localhost", 1883, 60)

    # Start MQTT loop
    print("Starting MQTT listener...")
    client.loop_forever()

except Exception as e:
    print(f"Error: {e}")