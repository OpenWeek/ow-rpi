# Openweek Raspberry Pi's Weather Station
# Copyright c 2018  
# Benjamin De Cnuydt, Quentin Delmelle, Robin Descamps
# Colin Evrard, Maxime Franco, Lucas Ody, 
# Maxime Postaire, Nicolas Rybowski, Antoine Vanderschueren.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import SI1132
import BME280
import sys
import time
import os
import threading
import paho.mqtt.client as mqtt
import yaml
import argparse

#default device
device = "i2c-1"
pi_id = None

si1132 = SI1132.SI1132(device)
bme280 = BME280.BME280(device, 0x03, 0x02, 0x02, 0x02)

client = None

broker = 'localhost'
port = 1883
timeStep = 300
pi_id = 0
data = {}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

class ReadAndSend(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self, timeStep):
        while True:
	    ts = int(time.time())
            p = bme280.read_pressure()
            client.publish("OWRPI/temperature", str(pi_id) + " - " + str(ts) + " - " + str(bme280.read_temperature()))
            client.publish("OWRPI/humidity", str(pi_id) + " - " + str(ts) + " - " +str( bme280.read_humidity() ))
            client.publish("OWRPI/pressure", str(pi_id) + " - " + str(ts) + " - " + str(p/100.0))
            client.publish("OWRPI/infrared", str(pi_id) + " - " + str(ts) + " - " + str(si1132.readIR()))
            client.publish("OWRPI/ultraviolet", str(pi_id) + " - " + str(ts) + " - " + str(si1132.readUV() / 100.0))
            client.publish("OWRPI/luminosity", str(pi_id) + " - " + str(ts) + " - " + str(int(si1132.readVisible())))

            #print "UV_index : %.2f" % (si1132.readUV() / 100.0)
            #print "Visible :", int(si1132.readVisible()), "Lux"
            #print "IR :", int(si1132.readIR()), "Lux"

            time.sleep(timeStep)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect data from (multiple ?) raspberri pi using mqtt')
    parser.add_argument('--port', '-p', action='store', type=int, help='network port to connect to (default is 1883)')
    parser.add_argument('--host', '-H', action='store', help='mqtt host to connect to (default is localhost)')
    parser.add_argument('--timeStep', '-t', action='store', type=int, help='frequency of data sending in seconds (default is 300)')
    parser.add_argument('--id', action='store', type=int, help='set the pi\'s id (default is 0)')
    args = parser.parse_args()

    try:
        with open("../config/weather_board.yaml", 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    except IOError as exc:
        print(exc)
    
    if args.host == None:
        if 'BROKER' in data:
            broker = data['BROKER']
    else:
        broker = args.host

    if args.port == None:
        if 'BROKER_PORT' in data:
            port = data['BROKER_PORT']
    else:
        port = args.port

    if args.timeStep == None:
        if 'TIMESTEP' in data:
            timeStep = data['TIMESTEP']
    else:
        timeStep = args.timeStep
    
    if args.id == None:
        if 'ID' in data:
            pi_id = data['ID']
    else:
        pi_id = args.id

    client = mqtt.Client("owid2")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker,port, timeStep*2)

    loop = ReadAndSend()
    loop.run(timeStep)
