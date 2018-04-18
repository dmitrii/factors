import webapp2
from datetime import date, datetime
from sympy.ntheory import factorint
from google.appengine.ext import ndb

class Factors(ndb.Model): # id = number to be factored
    request_ts = ndb.DateTimeProperty(auto_now_add=True)
    result_ts = ndb.DateTimeProperty()
    result_msg = ndb.StringProperty()
    result_list = ndb.StringProperty(repeated=True)

class DoFactor(webapp2.RequestHandler):
    def post(self):
        number = self.request.get('number')
        f = Factors.get_by_id(number)

        f.result_list = []
        factors = factorint(int(number)) # do the calculation
        for k in factors.keys():
            f.result_list.append(str(k))
        f.result_msg = "computed"
        f.result_ts = datetime.now()
        f.put()

app = webapp2.WSGIApplication([
    ('/factor', DoFactor),
], debug=True)
