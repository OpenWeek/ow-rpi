import paho.mqtt.client as mqtt

broker = "test.mosquitto.org"
port = 1883
keepAlive = 60

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client("owid2")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker,port,keepAlive)

client.publish("OWRPI/temp",16.6)
client.publish("OWRPI/hum",0.23)
client.publish("OWRPI/press",999)
client.publish("OWRPI/IR",409)
client.publish("OWRPI/UV",0.1)

client.disconnect()
