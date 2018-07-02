#!/usr/bin/env python

import web
from jinja2 import Environment, FileSystemLoader

urls = ("/", "main",
        "/chart", "chart"
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


class chart:
    def GET(self):
        # TODO: request to api
        # web.header('Content-Type', 'text/??')
        user_input = web.input()

        return "plop"

class main:
    def GET(self):
        # TODO: get base values from api
        return render_template("chart.html", **context)


if __name__ == "__main__":
    web.config.debug = True
    app = web.application(urls, globals())
    app.run()
