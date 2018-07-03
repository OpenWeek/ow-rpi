#!/usr/bin/python
import SI1132
import BME280
import sys
import time
import os
import threading
import paho.mqtt.client as mqtt

broker = "test.mosquitto.org"
port = 1883
keepAlive = 60

#default device
device = "i2c-1"

si1132 = SI1132.SI1132(device)
bme280 = BME280.BME280(device, 0x03, 0x02, 0x02, 0x02)


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

class ReadAndSend(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            p = bme280.read_pressure()
            client.publish("OWRPI/temp",bme280.read_temperature())
            client.publish("OWRPI/hum",bme280.read_humidity())
            client.publish("OWRPI/press",p/100.0)
            client.publish("OWRPI/IR",si1132.readIR())
            client.publish("OWRPI/UV",(si1132.readUV() / 100.0))

            #print "UV_index : %.2f" % (si1132.readUV() / 100.0)
            #print "Visible :", int(si1132.readVisible()), "Lux"
            #print "IR :", int(si1132.readIR()), "Lux"
            #print "temperature : %.2f 'C" % bme280.read_temperature()
            #print "humidity : %.2f %%" % bme280.read_humidity()
            #print "pressure : %.2f hPa" % (p / 100.0)
            time.sleep(1)

loop = ReadAndSend()
loop.run()
