import json

import webapp2

from factoring_service.factors import Factors


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Welcome to factapp!')


class ListFactors(webapp2.RequestHandler):
    def get(self):
        offset = int(self.request.get("offset", default_value=0))
        limit = int(self.request.get("limit", default_value=10))
        results = [result.safe_dict()
                   for result in Factors.list(offset, limit)]
        self.response.headers['Content-Type'] = 'text/json'
        json.dump(results, self.response, indent=4)


class GetFactor(webapp2.RequestHandler):
    def get(self, number):
        result = Factors.get_or_start_factoring(number)
        self.response.headers['Content-Type'] = 'text/json'
        json.dump(result.safe_dict(), self.response, indent=4)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/factors', ListFactors),
    ('/factors/(\d+)', GetFactor),
], debug=True)
