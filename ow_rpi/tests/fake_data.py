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
import os
import random as rd

if __name__ == '__main__':
    interval = 365*24*3600
    now = int(time.time())
    start = now-interval

    for t in range(start, now, 30):
        save_measure(0, 'temperature', t, 18+float(rd.randint(-1000,1000))/10000)
        save_measure(0, 'pressure', t, 1000+float(rd.randint(-1000,1000))/1000)
        save_measure(0, 'humidity', t, 68+float(rd.randint(-1000,1000))/10000)
        save_measure(0, 'luminosity', t, 1000+float(rd.randint(-1000,1000))/10000)
        save_measure(0, 'infrared', t, 29+float(rd.randint(-1000,1000))/1000)
        save_measure(0, 'ultraviolet', t, 0.02+float(rd.randint(-1000,1000))/1000000)
        save_measure(1, 'temperature', t, 18+float(rd.randint(-1000,1000))/10000)
        save_measure(1, 'pressure', t, 1000+float(rd.randint(-1000,1000))/1000)
        save_measure(1, 'humidity', t, 68+float(rd.randint(-1000,1000))/10000)
        save_measure(1, 'luminosity', t, 1000+float(rd.randint(-1000,1000))/10000)
        save_measure(1, 'infrared', t, 29+float(rd.randint(-1000,1000))/1000)
        save_measure(1, 'ultraviolet', t, 0.02+float(rd.randint(-1000,1000))/1000000)
