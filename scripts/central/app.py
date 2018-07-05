#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json
from db_handler import *
from jinja2 import Environment, FileSystemLoader

urls = ("/", "chart",
        "/chart","update_quick_chart",
        "/update","update_chart"
)

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', [])

    jinja_env = Environment(
            loader = FileSystemLoader("../../templates"),
            extensions=extensions
    )

    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)

class update_quick_chart:
    def GET(self):
        web.header('Content-Type', 'application/json')
        last_time = web.input().last
        print last_time

        def my_filter(arr):
            print arr
            arr2 =  [x for x in arr if x['x'] > last_time]
            print arr2
            return arr2
        measures =  {
            "TEMPERATURE": my_filter(get_measure_now("temperature")),
            # "HUMIDITY": [
            #     {'x': 1530542690000, 'y':0.2},
            #     {'x': 1530542760000, 'y':0.4}
            # ],
            "PRESSURE":  my_filter(get_measure_now("pressure"))
        }# get_measure_all("TEMPERATURE")
        # TODO: get right values
        return json.dumps(measures)

class update_chart:
    def GET(self):
        web.header('Content-Type', 'application/json')
        format = int(web.input().format)
        ALL_FORMATS = [get_measure_now, get_measure_hour, get_measure_day, get_measure_week, get_measure_month]

        format_f = ALL_FORMATS[format]

        measures =  {
            "TEMPERATURE": format_f("temperature")
            # [
            #     {'x': 1530342750000, 'y':32},
            #     {'x': 1530442755000, 'y':30},
            #     {'x': 1530542760000, 'y':35}
            # ]
            ,
            # "HUMIDITY": [
            #     {'x': 1530342750000, 'y':0.3},
            #     {'x': 1530442757000, 'y':0.7},
            #     {'x': 1530542760000, 'y':0.4}
            # ],
            "PRESSURE": format_f("pressure")
            # [
            #     {'x': 1530342750000, 'y':980},
            #     {'x': 1530442758000, 'y':1003},
            #     {'x': 1530542760000, 'y':995}
            # ]
        }# get_measure_all("TEMPERATURE")
        # TODO: get right values
        return json.dumps(measures)

class chart:
    def GET(self):
        # TODO: get base values from api
        context = {
                "chart_data": json.dumps(
                    {
                        "TEMPERATURE": get_measure_now("temperature")
                        # [
                        #     {'x': 1530542612000, 'y':20},
                        #     {'x': 1530542622000, 'y':25},
                        #     {'x': 1530542698000, 'y':22}
                        # ]
                        ,
                        # "HUMIDITY":
                        # [
                        #     {'x': 1530542645000, 'y':0.3},
                        #     {'x': 1530542667000, 'y':0.7},
                        #     {'x': 1530542685000, 'y':0.6}
                        # ]
                        # ,
                        "PRESSURE": get_measure_now("pressure")
                        # [
                        #     {'x': 1530542602000, 'y':1050},
                        #     {'x': 1530542647000, 'y':995},
                        #     {'x': 1530542649000, 'y':1003}
                        # ]
                    }),
                "data_params": json.dumps(
                    {
                        "names": ["TEMPERATURE", "PRESSURE",], # "HUMIDITY"],
                        "labels": ["Temperature", "Pressure", "Humidity"],
                        "units": ["°C", "hPa", "%"],
                        "colors": ["red", "green", "blue"],
                        "positions": ["left", "right", "right"],
                        "mins": [15, 990, 0.2],
                        "maxs": [30, 1120, 0.7]
                    }
                )
                }
        return render_template("chart.html", **context)


if __name__ == "__main__":
    web.config.debug = True
    app = web.application(urls, globals())
    app.run()
