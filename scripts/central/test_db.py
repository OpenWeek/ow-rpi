import db_handler as db
import time
import unittest
import os

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.interval = 7*24*3600
        self.start = int(time.time()) - self.interval
        self.name1 = "test_temperature"
        self.name2 = "test_pressure"
        self.suffix = ".rrd"

        temp_base = 10
        temp_mul = 0.01
        pressure_base = 1000
        pressure_mul = 0.1

        db.init_measure(self.name1, temp_base, 1+temp_base+temp_mul*(self.interval/300))
        db.init_measure(self.name2, pressure_base, 1+pressure_base+pressure_mul*(self.interval/300))

        for t in range(1+self.interval/300):
            db.save_measure(self.name1, self.start+t*300, temp_base+temp_mul*t)
            db.save_measure(self.name2, self.start+t*300, pressure_base+pressure_mul*t)

    def test_save_measure(self):
        self.assertTrue(os.path.exists("../../storage"))
        self.assertTrue(os.path.isfile("../../storage/"+self.name1+self.suffix))
        self.assertTrue(os.path.isfile("../../storage/"+self.name2+self.suffix))
    #should find only one None at the end of the list because there is no measure recorded yet
    #
    
    def test_no_None(self):
        none_count = 0
        measures = db.get_measure_from(self.name1, self.interval)
        for elem in measures:
            if elem["y"] is None:
                none_count+=1
        self.assertLessEqual(none_count, 1, "start is: "+str(self.start)+" and measures are: "+str(measures))

    def test_None_out_of_range(self):
        name = "test_None_out_of_range"
        db.init_measure(name, 0, 0)
        for t in range(self.interval/300):
            db.save_measure(name, self.start+t*300, 1000)
        for elem in db.get_measure_from(name, self.interval):
            self.assertIsNone(elem["y"], "the bounds are not working")
    
if __name__ == '__main__':
    unittest.main()
