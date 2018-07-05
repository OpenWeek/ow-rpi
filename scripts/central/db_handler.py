import json
import fcntl
import rrdtool
import os
"""
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
"""

def init_measure(name, min, max):
    rrdtool.create(
        "../../storage/"+name+".rrd",
        "--start", "-1y",
        "--step", "30",
        "RRA:LAST:0.5:1:10",
        "RRA:AVERAGE:0.5:10:12",
        "RRA:AVERAGE:0.5:120:24",
        "RRA:AVERAGE:0.5:2880:7",
        "RRA:AVERAGE:0.5:20160:4",
        "RRA:AVERAGE:0.5:80640:12",
        "DS:measure:GAUGE:3600:"+str(min)+":"+str(max))

def save_measure(measure, time, value):

    rrdtool.update("../../storage/"+measure.lower()+".rrd", str(time)+":"+str(value))

def get_measure_now(measure):
    return get_measure_from(measure, 300)

def get_measure_minute(measure):
        return get_measure_from(measure, 3600)

def get_measure_hour(measure):
    return get_measure_from(measure, 24*3600)

def get_measure_day(measure):
    return get_measure_from(measure, 7*24*3600)

def get_measure_week(measure):
    return get_measure_from(measure, 4*7*24*3600)

def get_measure_month(measure):
    return get_measure_from(measure, 12*4*7*24*3600)
    
def delete_measure(measure):
    path = "../../storage/"+measure.lower()+".rrd"
    try:
        if os.path.isfile():
            os.remove(path)
        else:    
            print("Error: %s file not found" % path)
    except OSError, e:  
        print ("Error: %s - %s." % (e.filename, e.strerror))


def get_measure_from(measure, interval):
    """
    Get all entries of the desired measure (temperature, pression, humidity, ...) from Database (rrd)
    recorded in the last <interval> seconds.
    """

    result = rrdtool.fetch("../../storage/"+measure+".rrd", "AVERAGE", "-a", "-r", "30", "-s", str(-interval), "-e", "now")

    start, end, step = result[0]
    ds = result[1]
    rows = result[2]
    ret = []
    ts = start + 30
    for i in range(len(rows)):
	    ret.append({})
	    ret[i]['x'] = ts*1000
	    ret[i]['y'] = rows[i][0]
	    ts += step

    print("{} {} {}".format(start, end, step))
    return ret
