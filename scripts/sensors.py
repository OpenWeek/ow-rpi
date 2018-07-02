from Adafruit_BME280 import *
import threading

class UpdateSensors(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        sensor = BME280(p_mode=BME280_OSAMPLE_8, t_mode=BME280_OSAMPLE_2, h_mode=BME280_OSAMPLE_1, filter=BME280_FILTER_16)
        tstart = time.time()
        
    def run(self):
        while (stdscr.getch() == -1) :
            degrees = sensor.read_temperature()
            pascals = sensor.read_pressure()
            hectopascals = pascals / 100
            humidity = sensor.read_humidity()
            time.sleep(1)

test = UpdateSensors()
test.run()
