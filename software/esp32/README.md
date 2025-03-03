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
 
 OR
 
/opt/homebrew/opt/mosquitto/sbin/mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf
```

To test it, open a terminal and type
```
mosquitto_sub -v -t 'test/topic'
```

Then in a second terminal type
```
mosquitto_pub -t 'test/topic' -m 'helloWorld'
```

And the first terminal should recieve the message.


To make the MQTT server available on the web you'll have to do port forwarding from you router.

Finally you can launch MQTT Explorer (for example) and connect to 192.168.8.187:1883 to recieve the data.
Then you can send message through the internet with the command

```
mosquitto_pub -h 192.168.8.187 -t 'test/topic' -m 'helloWorld'
```

For now, the mosquitto server is only there to display various data that we may need, especially when developping.


# How to upload code through the net  

The CircuitPython web workflow has been activate, so just go to the board's ip address and upload your code from there. Ex: 

192.168.8.118/fs
192.168.8.118/code


