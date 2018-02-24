#!/usr/bin/env python
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        num_input = float(self.request.get("numinp"))
        conversion = self.request.get("conversion")

        result = None

        if conversion == "1":
            result = num_input * 0.621371
        elif conversion == "2":
            result = num_input * 1.60934

        params = {'result': result}

        return self.render_template('result.html', params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
