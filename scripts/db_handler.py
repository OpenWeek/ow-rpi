import json

"""
JSON format:

{
    "measure": {
                "timestamp-1": 28.5
                "timestamp-2": 30.0
                }
    "measure2": {
                "timestamp-1": 0.3
                "timestamp-2": 0.7
                }
}

"""

def save_measure(measure, time, value):
    """
    Save the measure (Temperature, Pression or Humidity) in Database (JSON),
    with the time it was recorded, and its value. Returns 0 if the measure is
    saved, -1 otherwise
    """

    if measure!="TEMPERATURE" and measure != "PRESSURE" and measure != "HUMIDITY":
        return -1

    measures = dict()

    temperature_file = open('../storage/measures.json', 'r')
    try:
        measures = json.load(temperature_file)
    finally:
        temperature_file.close()

    measures[measure][time] = value

    temperature_file = open('../storage/measures.json', 'w')
    try:
        json.dump(measures, temperature_file)
    finally:
        temperature_file.close()

    return 0


def get_measure_all(measure):
    """
    Get the desired measure (Temperature, Pression or Humidity) from Database (JSON):
    all the data that are recorded in a Dictionary (time, value)
    """

    if measure!="TEMPERATURE" and measure != "PRESSURE" and measure != "HUMIDITY":
        print("error "+measure)
        return -1

    measures = dict()

    measure_file = open('../storage/measures.json', 'r')
    try:
        measures = json.load(measure_file)
    finally:
        measure_file.close()

    return measures[measure]
