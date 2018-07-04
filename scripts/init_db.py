import db_handler as db

if __name__ == '__main__':

    db.init_measure('temperature', -273.15, 200)
    db.init_measure('pressure', 800, 1300)
    db.init_measure('luminosity', 0, 150000)
    db.init_measure('humidity', 0, 5000)
    db.init_measure('ultraviolet', 0, 5000)
    db.init_measure('infrared', 0, 5000)
