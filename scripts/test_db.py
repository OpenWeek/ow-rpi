import db_handler as db
import time

if __name__ == '__main__':

    interval = 24*3600
    start = time.time() - interval

    """
    for t in range(interval/300):
        db.save_measure("temperature", start+t*300, 10+0.01*t)
        db.save_measure("pressure", start+t*300, 1000+0.1*t)
    """

    print(db.get_measure_from("temperature", interval))
    print(db.get_measure_from("pressure", interval))
