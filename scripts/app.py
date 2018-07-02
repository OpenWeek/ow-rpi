#!/usr/bin/env python

import web
import json
from jinja2 import Environment, FileSystemLoader

urls = ("/", "chart",
        "/test", "test"
)

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', [])

    jinja_env = Environment(
            loader = FileSystemLoader("../templates"),
            extensions=extensions
    )


    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)


class hello:
    def GET(self):
        context = {
                "value1" : "Python",
                "value2" : "Jinja2"
                }
        return render_template("index_template.html", **context)

class test:
    def GET(self):
        return "Hello world from python"


class update_quick_chart:
    def GET(self):
        web.header('Content-Type', 'application/json')
        last_time = web.input()
        measures = get_measure_all("TEMPERATURE")
        # TODO: get right values
        return json.dumps(measures)

class chart:
    def GET(self):
        # TODO: get base values from api
        context = {
                "value1" : "Python",
                "value2" : "Jinja2",
                "base_chart_data": json.dumps(
                    {
                        "TEMPERATURE": [
                            {'x': 1, 'y':20},
                            {'x': 3, 'y':25},
                            {'x': 7, 'y':22}
                        ],
                        "HUMIDITY": [
                            {'x': 0, 'y':0.3},
                            {'x': 3, 'y':0.7},
                            {'x': 8, 'y':0.6}
                        ],
                        "PRESSURE": [
                            {'x': 2, 'y':1050},
                            {'x': 4, 'y':995},
                            {'x': 7, 'y':1003}
                        ]
                    })
                }
        return render_template("chart.html", **context)


if __name__ == "__main__":
    web.config.debug = True
    app = web.application(urls, globals())
    app.run()
