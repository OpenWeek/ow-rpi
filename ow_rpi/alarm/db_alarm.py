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

import 	sqlite3
import time
import yaml
from ow_rpi.utils.send_email import *
from ow_rpi.utils.date import *

def get_config():
	with open("ow_rpi/config/alarm_config.yaml", 'r') as stream:
		try:
			return yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)

def get_database():
	config = get_config()
	conn = sqlite3.connect("ow_rpi/storage/"+config['database']['name'])
	return conn

def init_db():
	conn = get_database()
	c = conn.cursor()
	c.execute("DROP TABLE IF EXISTS log")
	c.execute("CREATE TABLE log (timestamp INT, measure TEXT, value REAL, station INT, degree TEXT)" )
	conn.commit()
	conn.close()
	
def save_log(timestamp, measure, value, station, degree):
	conn = get_database()
	c = conn.cursor()
	c.execute("INSERT INTO log VALUES ('"+ str(timestamp) +"', '"+ str(measure) +"', '"+ str(value) +"', '"+ str(station) + "','" + str(degree) + "' )" )
	conn.commit()
	conn.close()
	
def get_log_now(measure = None, station = None, gravity = None):
    now = get_now()
    return get_log_from( now -300, now, measure,station, gravity)

def get_log_minute(measure = None, station = None, gravity = None):
    return get_log_now(measure, station, gravity)

def get_log_hour(measure = None, station = None, gravity = None):
    now = get_now()
    return get_log_from(now -3600, now, measure, station, gravity)

def get_log_day(measure = None, station = None, gravity = None):
    now = get_now()
    return get_log_from(now - (24*3600), now,measure, station, gravity)

def get_log_week(measure = None, station = None, gravity = None):
    now = get_now()
    return get_log_from(now -(7*24*3600), now,measure, station, gravity)

def get_log_month(measure = None, station = None, gravity = None):
    now = get_now()
    return get_log_from( now -(4*7*24*3600), now, measure, station, gravity)
    
def get_log_from(start, end, measure = None, station = None, gravity = None):
	conn = get_database()
	c = conn.cursor()
	query = "SELECT * FROM log where "
	if measure != None :
		query +=  "measure = '"+ measure +"' AND "
	if station != None :
		query +=  "station = '"+ str(station) +"' AND "
	if gravity != None :
		query +=  "degree = '"+ str(gravity) +"' AND "
	query += str(start) +" <= timestamp AND timestamp <= " + str(end)
	test = c.execute(query)
	result = []
	for i in test:	
		result.append(i)
	conn.close()
	return result
	
def get_log_all(measure):
	conn = get_database()
	c = conn.cursor()
	test = c.execute("SELECT * FROM log where measure = '"+ measure  + "'")
	result = []
	for i in test:
		result.append(i)
	conn.close()
	return result	
	
def get_now():
	return int(time.time())

def generate_alarm(station, measure, timestamp, value):
	config = get_config()
	alarm = True
	gravity = 0
	subject = "ALARM FROM STATION : " + str(station) + " GRAVITY : "
	if float(value) <= float(config[measure]['MINMIN']):
		subject += "2 !!!"
		gravity = "2 !!!"
		save_log(timestamp, measure, value, station, -2)
	elif float(value) <= float(config[measure]['MIN']):
		subject += "1"
		gravity = "1"
		save_log(timestamp, measure, value, station, -1)
	elif float(value) >= float(config[measure]['MAXMAX']):
		subject += "2 !!!"
		gravity = "2 !!!"
		save_log(timestamp, measure, value, station, 2)
	elif float(value) >= float(config[measure]['MAX']):
		subject += "1"
		gravity = "1"
		save_log(timestamp, measure, value, station, 1)
	else:
		alarm = False
	text = "ALARM FROM : \n\tSTATION : "+ str(station) + "\n\tMEASURE : "+ str(measure)+ "\n\tVALUE : "+ str(value) + "\n\tGRAVITY : "+ str(gravity) + "\n\tDATE : "+ str(timestamp_to_date(int(timestamp)))
	
	if alarm:
		print config['list_email']
		send_mail(subject,text, config['list_email'])
