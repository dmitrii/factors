""" Represents the results of a prime factorization. """
from datetime import datetime

from google.appengine.api import taskqueue
from google.appengine.ext import ndb


class Factors(ndb.Model):
    """ Models the prime factors of an integer, which serves as the key. """
    request_ts = ndb.DateTimeProperty(auto_now_add=True)
    result_ts = ndb.DateTimeProperty(indexed=False)
    result_msg = ndb.StringProperty(default='pending', indexed=False)
    result_list = ndb.BlobProperty(repeated=True, indexed=False)

    @staticmethod
    @ndb.transactional
    def get_or_start_factoring(product):
        """ Starts a factoring job or retrieves the result. """
        key = ndb.Key(Factors, str(product))
        entity = key.get()
        if entity is not None:
            return entity

        result = Factors(key=key)
        result.put()

        taskqueue.add(url='/factor', target='factoring-service',
                      params={'number': product}, transactional=True)
        return result

    @staticmethod
    def list(offset, limit):
        query = Factors.query().order(-Factors.request_ts)
        return query.fetch(offset=offset, limit=limit)

    @staticmethod
    def set_result(product, result_list):
        key = ndb.Key(Factors, str(product))
        factors = key.get()
        factors.result_list = [str(result) for result in result_list]
        factors.result_msg = 'computed'
        factors.result_ts = datetime.utcnow()
        factors.put()

    @staticmethod
    def encode(value):
        return value.isoformat() if isinstance(value, datetime) else value

    def safe_dict(self):
        details = {'number': int(self.key.id())}
        details.update({key: self.encode(val)
                        for key, val in self.to_dict().items()})
        details['result_list'] = [int(result) for result in self.result_list]
        return details
