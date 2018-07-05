# Openweek Raspberry pi's weather station
# Copyright c 2018  Maxime Postaire, Lucas Ody, Maxime Franco,
# Nicolas Rybowski, Benjamin De Cnuydt, Quentin Delmelle, Colin Evrard,
# Antoine Vanderschueren.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# Openweek Raspberry pi's weather station
# Copyright c 2018  Maxime Postaire, Lucas Ody, Maxime Franco,
# Nicolas Rybowski, Benjamin De Cnuydt, Quentin Delmelle, Colin Evrard,
# Antoine Vanderschueren.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import SI1132
import BME280
import sys
import time
import os
import threading
import paho.mqtt.client as mqtt
import yaml

#default device
device = "i2c-1"

si1132 = SI1132.SI1132(device)
bme280 = BME280.BME280(device, 0x03, 0x02, 0x02, 0x02)

client = None

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
            client.publish("OWRPI/temperature", str(ts) + " - " + str(bme280.read_temperature()))
            client.publish("OWRPI/humidity", str(ts) + " - " +str( bme280.read_humidity() ))
            client.publish("OWRPI/pressure", str(ts) + " - " + str(p/100.0))
            client.publish("OWRPI/infrared", str(ts) + " - " + str(si1132.readIR()))
            client.publish("OWRPI/ultraviolet", str(ts) + " - " + str(si1132.readUV() / 100.0))
            client.publish("OWRPI/luminosity", str(ts) + " - " + str(int(si1132.readVisible())))

            #print "UV_index : %.2f" % (si1132.readUV() / 100.0)
            #print "Visible :", int(si1132.readVisible()), "Lux"
            #print "IR :", int(si1132.readIR()), "Lux"

            time.sleep(timeStep)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect data from (multiple ?) raspberri pi using mqtt')
    parser.add_argument('--port', '-p', action='store', default=1883, type=int, help='network port to connect to (default is 1883)')
    parser.add_argument('--host', '-H', action='store', default='localhost', help='mqtt host to connect to (default is localhost)')
    parser.add_argument('--timeStep', '-t', action='store', default=300, type=int, help='frequency of data sending in seconds (default is 300)')    
    
    try:
        with open("../config/weatherBoard.yaml", 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    except IOError as exc:
        print(exc)
    
    if 'BROKER' in data:
        broker = data['BROKER']
    if 'BROKER_PORT' in data:
        port = data['BROKER_PORT']
    if 'TIMESTEP' in data:
        timeStep = data['TIMESTEP']

    args = parser.parse_args()
    broker = args.host
    port = args.port
    timeStep = args.timeStep

    client = mqtt.Client("owid2")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker,port, timeStep*2)

    loop = ReadAndSend()
    loop.run(timeStep)
