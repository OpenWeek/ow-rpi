from Adafruit_BME280 import *
from db_handler import *
import threading
import time

class UpdateSensors(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sensor = BME280(p_mode=BME280_OSAMPLE_8, t_mode=BME280_OSAMPLE_2, h_mode=BME280_OSAMPLE_1, filter=BME280_FILTER_16)
        self.tstart = time.time()
        
    def run(self):
        while (True) :
            degrees = self.sensor.read_temperature()
            pascals = self.sensor.read_pressure()
            hectopascals = pascals / 100
            humidity = self.sensor.read_humidity()
            timestamp = int(time.time())
            print "time: " + str(timestamp) + " | temp: " + str(degrees) + \
            "°C | pressure: " + str(hectopascals) + "hPa | humidity: " + str(humidity) + "%"
            save_measure("TEMPERATURE", timestamp, degrees)
            save_measure("PRESSURE", timestamp, hectopascals)
            save_measure("HUMIDITY", timestamp, humidity)
            time.sleep(1)

test = UpdateSensors()
test.run()
