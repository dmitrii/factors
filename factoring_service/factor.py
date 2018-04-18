import webapp2
from sympy.ntheory import factorint

from factors import Factors


class DoFactor(webapp2.RequestHandler):
    def post(self):
        number = int(self.request.get('number'))
        factors = factorint(number) # do the calculation
        Factors.set_result(number, factors.keys())

app = webapp2.WSGIApplication([
    ('/factor', DoFactor),
], debug=True)
