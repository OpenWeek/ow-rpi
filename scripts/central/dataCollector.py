from Adafruit_BME280 import *
from db_handler import *
import threading
import time
import paho.mqtt.client as mqtt
import signal
import sys


broker = "130.104.78.204"
port = 1883
keepAlive = 60
timeStep = 300
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


'''class UpdateSensors(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #self.sensor = BME280(p_mode=BME280_OSAMPLE_8, t_mode=BME280_OSAMPLE_2, h_mode=BME280_OSAMPLE_1, filter=BME280_FILTER_16)
        self.tstart = time.time()
        
        client.connect(broker,port,keepAlive)
        client.loop_start()
        
    def __del__(self):
		client.loop_stop()
		client.disconnect()
        
    def run(self):
        while (True) :
            degrees = self.sensor.read_temperature()
            pascals = self.sensor.read_pressure()
            hectopascals = pascals / 100
            humidity = self.sensor.read_humidity()
            timestamp = int(time.time())
            print "time: " + str(timestamp) + " | temp: " + str(degrees) + \
            "deg C | pressure: " + str(hectopascals) + "hPa | humidity: " + str(humidity) + "%"
            save_measure("temperature", timestamp, degrees)
            save_measure("pressure", timestamp, hectopascals)
            save_measure("humidity", timestamp, humidity)
            time.sleep(timeStep)'''
            
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

