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

from ow_rpi.db_handler.db_handler import *
import time
import unittest
import os

class TestDBMethods(unittest.TestCase):
    def setUp(self):
        self.interval = 7*24*3600
        start = time.time() - self.interval
        self.name1 = "test_temperature"
        self.name2 = "test_pressure"
        self.suffix = ".rrd"
        self.pi_index = 0
        temp_base = 10
        temp_mul = 0.01
        pressure_base = 1000
        pressure_mul = 0.1

        init_measure(self.pi_index,self.name1)
        init_measure(self.pi_index,self.name2)

        for t in range(self.interval/300):
            save_measure(0, self.name1, start+t*300, temp_base+temp_mul*t)

    def test_save_measure(self):
        self.assertTrue(os.path.exists("ow_rpi/storage"))
        print "ow_rpi/storage/"+str(self.pi_index)+self.name1+self.suffix
        self.assertTrue(os.path.isfile("ow_rpi/storage/"+"pi"+str(self.pi_index)+"_"+self.name1+self.suffix))
        self.assertTrue(os.path.isfile("ow_rpi/storage/"+"pi"+str(self.pi_index)+"_"+self.name2+self.suffix))
    #should find only one None at the end of the list because there is no measure registered yet
    #
    def test_no_None(self):
        none_count = 0
        for elem in get_measure_from(0, self.name1, self.interval):
            if elem["y"] is None:
                none_count+=1
        
        self.assertLessEqual(none_count, 1)
        # string = str(db.get_measure_from(self.name1, self.interval))
        # has_none = string.find("None")
        # self.assertEqual(has_none, -1, string)


if __name__ == '__main__':
    unittest.main()
