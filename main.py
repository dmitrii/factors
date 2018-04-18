import webapp2
import json
from datetime import date, datetime
from google.appengine.ext import ndb
from google.appengine.api import taskqueue

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def write_response(response, list):
    reply = json.dumps(list, indent=4, default=json_serial)
    response.headers['Content-Type'] = 'text/json'
    response.write(reply)
        
class Factors(ndb.Model): # id = number to be factored
    request_ts = ndb.DateTimeProperty(auto_now_add=True)
    result_ts = ndb.DateTimeProperty()
    result_msg = ndb.StringProperty()
    result_list = ndb.StringProperty(repeated=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Welcome to factapp!')

class ListFactors(webapp2.RequestHandler):
    def get(self):
        offset = int(self.request.get("offset", default_value=0))
        limit = int(self.request.get("limit", default_value=10))

        q = Factors.query().order(-Factors.request_ts).fetch(offset=offset, limit=limit)
        list = [ ]
        for p in q: 
            list.append(dict(p.to_dict(), number=p.key.id()))
        write_response(self.response, list)

class GetFactor(webapp2.RequestHandler):
    def get(self, number):
        f = Factors.get_or_insert(number)
        if f.result_msg is None: # number not in DB
            f.result_msg = "pending"
            f.put()
            task = taskqueue.add( # check for queue errors?
                url = "/factor",
                target = "factoring-service",
                params = { 'number': number })

        list = [ dict(f.to_dict(), number=number) ]
        write_response(self.response, list)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/factors', ListFactors),
    ('/factors/(\d+)', GetFactor),
], debug=True)
