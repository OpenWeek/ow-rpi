#from Adafruit_BME280 import *
from db_handler import *
import threading
import time
import paho.mqtt.client as mqtt
import signal
import sys
import argparse


keepAlive = 300
client = None

def signal_handler(signal, frame):
    sys.exit(0)
      
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
    payload = msg.payload.split(" - ")
    
    if msg.topic == "OWRPI/temp" : 
        save_measure("temperature", payload[0], payload[1])
    elif msg.topic == "OWRPI/hum" : 
        save_measure("humidity", payload[0], payload[1])
    elif msg.topic == "OWRPI/press" : 
        save_measure("pressure", payload[0], payload[1])
    elif msg.topic == "OWRPI/IR" : 
        save_measure("infrared", payload[0], payload[1])
    elif msg.topic == "OWRPI/UV" : 
        save_measure("ultraviolet", payload[0], payload[1])
    elif msg.topic == "OWRPI/visible" : 
        save_measure("luminosity", payload[0], payload[1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect data from (multiple ?) raspberri pi using mqtt')
    parser.add_argument('--port', '-p', action='store', default=1883, type=int, help='network port to connect to (default is 1883)')
    parser.add_argument('--host', action='store', default='localhost', help='mqtt host to connect to (default is localhost)')
    args = parser.parse_args()
    broker = args.host
    port = args.port

    signal.signal(signal.SIGINT, signal_handler)

    client = mqtt.Client("owid1")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker,port,keepAlive)
    client.subscribe("OWRPI/temp")
    client.subscribe("OWRPI/hum")
    client.subscribe("OWRPI/IR")
    client.subscribe("OWRPI/UV")
    client.subscribe("OWRPI/press")
    client.subscribe("OWRPI/visible")
    client.loop_forever()
    #test = UpdateSensors()
    #test.run()

