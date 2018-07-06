#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Openweek Raspberry pi's weather station
# Copyright c 2018  Maxime Postaire, Lucas Ody, Maxime Franco,
# Nicolas Rybowski, Benjamin De Cnuydt, Quentin Delmelle, Colin Evrard,
# Antoine Vanderschueren.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import web
import json
from ow_rpi.db_handler.db_handler import *

from jinja2 import Environment, FileSystemLoader

urls = ("/", "chart",
        "/chart","update_quick_chart",
        "/update","update_chart"
)

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', [])

    jinja_env = Environment(
            loader = FileSystemLoader("ow_rpi/templates"),
            extensions=extensions
    )

    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)

'''
    @fun: a function returning data, that takes 2 args:
            - the pi-id
            - the measure-name
          in that order
    @pi_id: the id of the pi from which we want to extract the data
    @returns: a dictionary with the data for according to @fun from @pi-id for all measures in the config file
'''
def get_measures(fun, pi_id):
    with open("ow_rpi/config/chart.yaml", 'r') as file:
        try:
            complete_file = yaml.load(file)
            measures = complete_file['measures']

            chart_data = {}
            for key in measures.keys():
                chart_data[key] = fun(pi_id, key.lower())

            return chart_data

        except yaml.YAMLError as exc:
            print(exc)
            return {}

def get_parameters():
    with open("ow_rpi/config/chart.yaml", 'r') as file:
        try:
            complete_file = yaml.load(file)
            measures = complete_file['measures']
            parameters = complete_file['parameters']

            data_params = {}
            for param in parameters:
                data_params[param] = []
            data_params["name"] = []

            for key, values in measures.items():
                data_params["name"] += [key]
                for param, val in values.items():
                    data_params[param] += [val]

            return data_params

        except yaml.YAMLError as exc:
            print(exc)
            return {}

class update_quick_chart:
    def GET(self):
        web.header('Content-Type', 'application/json')
        last_time = int(web.input().last)

        def my_filter(arr):
            # TODO: do a continuous update, don't resend everything
            return  arr#[x for x in arr if x['x'] > last_time]

        measures = get_measures(get_measure_now, 0)
        return json.dumps([my_filter(x) for x in measures])

class update_chart:
    def GET(self):
        web.header('Content-Type', 'application/json')
        format = int(web.input().format)
        ALL_FORMATS = [get_measure_now, get_measure_hour, get_measure_day, get_measure_week, get_measure_month]

        measures =  get_measures(ALL_FORMATS[format], 0)
        return json.dumps(measures)

class chart:
    def GET(self):
        context = {
                "chart_data": json.dumps(get_measures(get_measure_now, 0)),
                "data_params": json.dumps(get_parameters())
                }
        return render_template("chart.html", **context)


if __name__ == "__main__":
    web.config.debug = True
    app = web.application(urls, globals())
    app.run()
