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

import db_handler as db
import time
import os
import random as rd

if __name__ == '__main__':
    interval = 365*24*3600
    now = int(time.time())
    start = now-interval

    for t in range(start, now, 30):
        var = float(rd.randint(-1000,1000))/10000
        var2 = float(rd.randint(-1000,1000))/1000
        db.save_measure(0, 'temperature', t, 18+var)
        db.save_measure(0, 'pressure', t, 1000+var2)
