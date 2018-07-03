import db_handler as db

if __name__ == '__main__':

    measures = ['temperature', 'pressure', 'humidity', 'luminosity', 'infrared', 'ultraviolet']

    for measure in measures:
        db.init_measure(measure)
