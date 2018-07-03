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
        "RRA:AVERAGE:0.5:12:288",
        "RRA:AVERAGE:0.5:288:2016",
        "RRA:AVERAGE:0.5:2016:8640",
        "DS:measure:GAUGE:3600:-5000:5000")

def save_measure(measure, time, value):

    rrdtool.update("../storage/station"+measure+".rrd", time+":"+str(value))


def get_measure_hour(measure):

    result = rrdtool.fetch("../storage/"+measure+".rrd", "AVERAGE", "-a", "-r", "5m", "-s", "end-1hour")
    start, end, step = result[0]
    ds = result[1]
    rows = result[2]

    print(rows)

def get_measure_from(measure, start_time):
    """
    Get all entries of the desired measure (Temperature, Pression or Humidity) from Database (JSON)
    whit key(-time-) > from:
    all the data that are recorded in a Dictionary (time, value)
    """

    measures = get_measure_all(measure)
