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

if __name__ == '__main__':

    interval = 7*24*3600
    start = time.time() - interval


    for t in range(interval/300):
        db.save_measure("temperature", start+t*300, 10+0.01*t)
        db.save_measure("pressure", start+t*300, 1000+0.1*t)


    print(db.get_measure_from("temperature", interval))
    print(db.get_measure_now("temperature"))
    print(db.get_measure_hour("temperature"))
    print(db.get_measure_day("temperature"))
    print(db.get_measure_week("temperature"))

    print(db.get_measure_from("pressure", interval))
