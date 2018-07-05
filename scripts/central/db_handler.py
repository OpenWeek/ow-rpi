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

import json
import fcntl
import rrdtool

def init_measure(name, min, max):
    rrdtool.create(
        "../../storage/"+name+".rrd",
        "--start", "-2h",
        "--step", "300",
        "RRA:LAST:0.5:1:12",
        "RRA:AVERAGE:0.5:12:24",
        "RRA:AVERAGE:0.5:288:7",
        "RRA:AVERAGE:0.5:2016:4",
        "RRA:AVERAGE:0.5:8064:12",
        "DS:measure:GAUGE:3600:"+str(min)+":"+str(max))

def save_measure(measure, time, value):

    rrdtool.update("../../storage/"+measure.lower()+".rrd", str(time)+":"+str(value))


def get_measure_now(measure):
    return get_measure_from(measure, 3600)

def get_measure_hour(measure):
    return get_measure_from(measure, 24*3600)

def get_measure_day(measure):
    return get_measure_from(measure, 7*24*3600)

def get_measure_week(measure):
    return get_measure_from(measure, 4*7*24*3600)

def get_measure_month(measure):
    return get_measure_from(measure, 12*4*7*24*3600)

def get_measure_from(measure, interval):
    """
    Get all entries of the desired measure (temperature, pression, humidity, ...) from Database (rrd)
    recorded in the last <interval> seconds.
    """

    result = rrdtool.fetch("../../storage/"+measure+".rrd", "AVERAGE", "-a", "-r", "300", "-s", str(-interval), "-e", "now")

    start, end, step = result[0]
    ds = result[1]
    rows = result[2]
    ret = []
    ts = start + 300
    for i in range(len(rows)):
	    ret.append({})
	    ret[i]['x'] = ts
	    ret[i]['y'] = rows[i][0]
	    ts += step

    #print("{} {} {}".format(start, end, step))
    return ret
