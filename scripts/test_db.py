import db_handler as db

if __name__ == '__main__':

    db.save_measure("temperature", 30.5)
    db.save_measure("temperature", 27)
    db.save_measure("temperature", 28.7)
    db.save_measure("temperature", 29.4)
    db.save_measure("temperature", 30.5)
    db.save_measure("temperature", 27)
    db.save_measure("temperature", 28.7)
    db.save_measure("temperature", 29.4)
    db.save_measure("pressure", 1013)
    db.save_measure("pressure", 1025)
    db.save_measure("pressure", 1056)
    db.save_measure("pressure", 1006)

    db.get_measure_hour("temperature")
    db.get_measure_hour("pressure")






    """
    temperatures = dict()

    temperatures['13:00'] = 30.0
    temperatures['14:00'] = 29.0
    temperatures['15:00'] = 29.5
    temperatures['16:00'] = 30.0
    temperatures['17:00'] = 27.0

    measures = dict()
    measures["TEMPERATURE"] = temperatures

    measure_file = open('../storage/measures.json', 'w')
    try:
        json.dump(measures, measure_file)
    finally:
        measure_file.close()

    measures_all = db.get_measure_all("TEMPERATURE")
    print(measures_all)

    db.save_measure("TEMPERATURE", '18:00', 25.5)
    measures_all_modified = db.get_measure_all("TEMPERATURE")
    print(measures_all_modified)
    """
