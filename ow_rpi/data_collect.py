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

from ow_rpi.db_handler.db_handler import *
import threading
import time
import paho.mqtt.client as mqtt
from ow_rpi.alarm.db_alarm import *
import signal
import sys
import argparse
import yaml

broker = 'localhost'
port = 1883
keepalive = 300
data = {}
client = None
channel = "OWRPI/"
measures = ["temperature", "humidity", "pressure", "infrared", "ultraviolet", "luminosity"]

def signal_handler(signal, frame):
    sys.exit(0)
      
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
    payload = msg.payload.split(" - ")
    for m in measures :
		if msg.topic == channel + m :
			save_measure(payload[0],m,payload[1],payload[2])
                        generate_alarm(0,m,payload[1],payload[2])
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect data from (multiple ?) raspberri pi using mqtt')
    parser.add_argument('--port', '-p', action='store', type=int, help='network port to connect to (default is 1883)')
    parser.add_argument('--host', '-H', action='store', help='mqtt host to connect to (default is localhost)')
    parser.add_argument('--keepalive', '-k', action='store', type=int, help='time while the connection is maintained when no data is transmitted in seconds (default is 300)')
    args = parser.parse_args()

    try:
        with open("./config/data_collect.yaml", 'r') as stream:
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
    
    if args.keepalive == None:
        if 'BROKER_KEEPALIVE' in data:
            keepalive = data['BROKER_KEEPALIVE']
    else:
        keepalive = args.keepalive

    
signal.signal(signal.SIGINT, signal_handler)

client = mqtt.Client("owid1")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, keepalive)
for m in measures :
	client.subscribe(channel + m)
client.loop_forever()


