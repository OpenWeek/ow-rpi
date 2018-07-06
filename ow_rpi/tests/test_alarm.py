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

from ow_rpi.alarm.db_alarm import *
import unittest
import os

class TestDBMethods(unittest.TestCase):
    def setUp(self):
		self.measure_temp = "temperature"
		self.pi_id = 0
		init_db()
		generate_alarm(self.pi_id, self.measure_temp, 1530807202, 14)
		generate_alarm(self.pi_id, self.measure_temp, 1530807202, 16)
		generate_alarm(self.pi_id, self.measure_temp, 1530807202, 21)
		generate_alarm(self.pi_id, self.measure_temp, 1530807202, 23)

    def test_alarm1(self):
		mytest = [['2018-07-05 18:13:22', u''+self.measure_temp, 14.0, 0, u'-2'], ['2018-07-05 18:13:22', u''+self.measure_temp, 16.0, 0, u'-1'], ['2018-07-05 18:13:22', u''+self.measure_temp, 21.0, 0, u'1'], ['2018-07-05 18:13:22', u''+self.measure_temp, 23.0, 0, u'2']]
		
		values = get_log_all(self.measure_temp)
		print values
		for i in range(len(values)):
			for j in range(len(values[i])):
				self.assertEqual(mytest[i][j], values[i][j])

if __name__ == '__main__':
    unittest.main()

# init_db()
# generate_alarm(0,"temperature", 1530807202, 14)
# generate_alarm(1,"temperature", 1530807202, 16)
# generate_alarm(0,"humidity", 1530807202, 21)
# generate_alarm(1,"humidity", 1530807202, 23)
# values = get_log_all()
# print values