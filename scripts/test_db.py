import db_handler as db
import time

if __name__ == '__main__':
<<<<<<< HEAD

    start = 1534463400
    """
    for t in range(7*24*3600/5):
        db.save_measure("temperature",start+t*300, 10+0.01*t)
        db.save_measure("pressure", start+t*300, 1000+0.1*t)
    """
    db.get_measure_week("temperature")
    db.get_measure_week("pressure")
=======

    interval = 3600
    start = time.time() - interval

    
    for t in range(12):
	print(t)
        db.save_measure("temperature", start+t*300, 10+0.01*t)
        db.save_measure("pressure", start+t*300, 1000+0.1*t)
    
>>>>>>> e620696eaaf1ef554df3777c7a60a2d18cbc6c9d

    print(db.get_measure_from("temperature", interval))
    print(db.get_measure_from("pressure", interval))
