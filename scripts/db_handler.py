import json
import fcntl
import rrdtool

def init_measure(name):
    rrdtool.create(
        "../storage/"+name+".rrd",
        "--start", "now",
        "--step", "300",
        "RRA:LAST:0.5:1:12",
        "RRA:AVERAGE:0.5:1:12",
        "RRA:AVERAGE:0.5:12:24",
        "RRA:AVERAGE:0.5:288:7",
        "RRA:AVERAGE:0.5:2016:4",
        "DS:measure:GAUGE:3600:-5000:5000")

def save_measure(measure, time, value):

    rrdtool.update("../storage/"+measure.lower()+".rrd", str(time)+":"+str(value))


def get_measure_hour(measure):

    result = rrdtool.fetch("../storage/"+measure+".rrd", "AVERAGE", "-a", "-r", "300", "-s", "-1hour")

    start, end, step = result[0]
    ds = result[1]
    rows = result[2]

    print("{} {} {}".format(start, end, step))
    return rows

def get_measure_week(measure):

    result = rrdtool.fetch("../storage/"+measure+".rrd", "AVERAGE", "-a", "-r", "300", "-s", "now", "-e", "+1week")

    start, end, step = result[0]
    ds = result[1]
    rows = result[2]

    print("{} {} {}".format(start, end, step))
    return rows

def get_measure_from(measure, start_time):
    """
    Get all entries of the desired measure (Temperature, Pression or Humidity) from Database (JSON)
    whit key(-time-) > from:
    all the data that are recorded in a
    """

    result = rrdtool.fetch("../storage/"+measure+".rrd", "AVERAGE", "-a", "-r", "300", "-s", start_time, "-e", "now")

    start, end, step = result[0]
    ds = result[1]
    rows = result[2]

    print("{} {} {}".format(start, end, step))
    return rows
