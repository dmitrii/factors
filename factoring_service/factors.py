""" Represents the results of a prime factorization. """
from __future__ import division

from datetime import datetime

from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
from google.appengine.api.taskqueue.taskqueue import TaskRetryOptions

# The number of seconds to keep queries cached.
QUERY_CACHE_TTL = 10


class Factors(ndb.Model):
    """ Models the prime factors of an integer, which serves as the key. """
    request_ts = ndb.DateTimeProperty(auto_now_add=True)
    result_ts = ndb.DateTimeProperty(indexed=False)
    result_msg = ndb.StringProperty(default='pending', indexed=False)
    result_list = ndb.BlobProperty(repeated=True, indexed=False)
    compute_duration = ndb.FloatProperty()
    result_list_size = ndb.IntegerProperty()

    @staticmethod
    @ndb.transactional
    def get_or_start_factoring(product):
        """ Starts a factoring job or retrieves the result. """
        key = ndb.Key(Factors, str(product))
        entity = key.get()
        if entity is not None:
            return entity

        entity = Factors(key=key)
        entity.put()
        taskqueue.add(url='/factor',
                      target='factoring-service',
                      params={'number': product},
                      transactional=True,
                      retry_options=TaskRetryOptions(task_age_limit=50)) # don't retry long-running tasks
        return entity

    @staticmethod
    def list(offset, limit):
    #    return Factors.list_by_result_size(offset, limit);
        cache_key = ':'.join(['-request_ts', str(offset), str(limit)])
        results = memcache.get(cache_key)
        if results is None:
            query = Factors.query().order(-Factors.request_ts)
            results = query.fetch(offset=offset, limit=limit)
            memcache.add(cache_key, results, QUERY_CACHE_TTL)

        return results

    @staticmethod
    def list_by_compute_duration(offset, limit):
        return Factors.gql(
            'ORDER BY compute_duration DESC '
            'LIMIT {} '
            'OFFSET {}'.format(limit, offset)
        )

    @staticmethod
    def list_by_result_size(offset, limit):
        return Factors.gql(
            'ORDER BY result_list_size DESC '
            'LIMIT {} '
            'OFFSET {}'.format(limit, offset)
        )

    @staticmethod
    def list_by_key(offset, limit):
        return Factors.gql(
            'ORDER BY __key__ '
            'LIMIT {} '
            'OFFSET {}'.format(limit, offset)
        )

    @staticmethod
    def set_result(product, result_list):
        key = ndb.Key(Factors, str(product))
        current_time = datetime.utcnow()
        factors = key.get()
        factors.result_list = [str(result) for result in result_list]
        factors.result_msg = 'computed'
        factors.result_ts = current_time
        duration = current_time - factors.request_ts
        factors.compute_duration = duration.microseconds / 1000000
        factors.result_list_size = len(factors.result_list)
        factors.put()

    @staticmethod
    def encode(value):
        return value.isoformat() if isinstance(value, datetime) else value

    def safe_dict(self):
        details = {'number': str(self.key.id()), # return as str() so JS doesn't convert to scientific notation
                   'now_ts': self.encode(datetime.utcnow())}
        details.update({key: self.encode(val)
                        for key, val in self.to_dict().items()})
        details['result_list'] = [int(result) for result in self.result_list]
        return details
