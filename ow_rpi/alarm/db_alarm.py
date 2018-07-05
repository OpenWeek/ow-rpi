import 	sqlite3
import time
import yaml

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
	
def get_log_now(measure):
    now = get_now()
    return get_log_from(measure, now -300, now)

def get_log_minute(measure):
    return get_log_now(measure)

def get_log_hour(measure):
    now = get_now()
    return get_log_from(measure, now -3600, now)

def get_log_day(measure):
    now = get_now()
    return get_log_from(measure, now - (24*3600), now)

def get_log_week(measure):
    now = get_now()
    return get_log_from(measure, now -(7*24*3600), now)

def get_log_month(measure):
    now = get_now()
    return get_log_from(measure, now -(4*7*24*3600), now)
    
def get_log_from(measure, start, end):
	conn = get_database()
	c = conn.cursor()
	print "SELECT * FROM log where measure = '"+ measure +"' AND '"+ str(start) +"' <= timestamp AND timestamp <= '" + str(end) + "'"
	test = c.execute("SELECT * FROM log where measure = '"+ measure +"' AND "+ str(start) +" <= timestamp AND timestamp <= " + str(end) )
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
	if float(value) <= float(config[measure]['MINMIN']):
		save_log(timestamp, measure, value, station, 2)
	elif float(value) <= float(config[measure]['MIN']):
		save_log(timestamp, measure, value, station, 1)
	elif float(value) >= float(config[measure]['MAXMAX']):
		save_log(timestamp, measure, value, station, 2)
	elif float(value) >= float(config[measure]['MAX']):
		save_log(timestamp, measure, value, station, 1)
