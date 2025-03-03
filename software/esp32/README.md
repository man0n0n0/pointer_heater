# How to run the MQTT server  

First, start an MQTT server on your computer. Make sure the mosquitto.conf contains those lines:

```
listener 1883 0.0.0.0
allow_anonymous true
```

That will assure you can connect to the broker through internet.

Next, start the MQTT server. On mac, run the command:

```
brew services start mosquitto
```

For now, the mosquitto server is only there to display various data that we may need, especially when developping.


# How to upload code through the net  

The CircuitPython web workflow has been activate, so just go to the board's ip address and upload your code from there. Ex: 

192.168.8.118/fs
192.168.8.118/code


