# ow-rpi

## getting started

1) This project requires a mqtt broker server for the RPi's to communicate. Install your own or use a free one (e.g. [mosquitto](http://test.mosquitto.org/))
2) Install the paho mqtt python library on all
```
pip install paho-mqtt
```

3) Put in the broker address and port in the config files and run the scripts on the corresponding RPi

#### sensors station
the sensors folder contains scripts for collecting data from [weather2station](https://wiki.odroid.com/accessory/sensor/weather-board/weather-board), run weather_station.py. You can use this as a template for your own sensors' scripts

#### central station
the central folder is used on the machine which centralizes data, has the database and run the webapp.
   * run the dataCollector.py script to collect data from sensors RPi's.
   * launch the lighttpd wep app, while in root of the project with the command.

```
lighttpd -D -f lighttpd.conf
```
