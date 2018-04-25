import webapp2
from sympy.ntheory import factorint

from factors import Factors

class DoFactor(webapp2.RequestHandler):

    def post(self):
        from google.appengine.runtime import DeadlineExceededError

        number = int(self.request.get('number'))
        try:
            factors = factorint(number, limit=10000000)  # do the calculation
            Factors.set_result(number, factors.keys(), 'computed')
        except DeadlineExceededError:
            print "computation took too long for " + number
            Factors.set_result(number, [], 'timed out')

app = webapp2.WSGIApplication([
    ('/factor', DoFactor),
], debug=True)
