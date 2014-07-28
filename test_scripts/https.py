# tom hensel <tom@jitter.eu> for CIPHRON

import requests
import hashlib
import time
import random

class NotConfiguredException(Exception):
    pass

class LoadTest(object):
    def __init__(self):
        # self.custom_timers = {}
        raise NotConfiguredException('foo')

    def run(self):
        # start measurement
        start_timer = time.time()

        # initialize session
        s = requests.Session()
        s.max_redirects = self.http_max_redirects
        s.headers = self.http_headers
        s.verify = self.https_verify_cert

        # do request
        r = s.get(self.http_url, timeout=self.http_timeout, params=self.params)

        # stop measurement
        latency = time.time() - start_timer

        # store latency
        self.custom_timers[r.status_code] = latency

        # verbose info
        print 'url:', r.url, ', code:', r.status_code, ', reason:', r.reason, ', elapsed:', r.elapsed, 'hash:', hashlib.sha224(r.text).hexdigest()

        # asset response code of 200 (HTTP OK)
        assert (r.status_code == requests.codes.ok), 'Bad Response: HTTP Code %s' % r.status_code

        # assert known string in content
        #assert ('iav' in content), 'Text Assertion Failed'

class Transaction(LoadTest):
    def __init__(self):
        self.custom_timers = {}

        # configuration
        self.test_id = 'mib-jira.iavtech.net_ssl'
        self.http_headers = {'User-Agent': 'Mozilla/4.0 (compatible; Testing)'}
        self.http_timeout = 5
        self.http_max_redirects = 10
        self.https_verify_cert = False
        self.http_url = 'https://mib-jira.iavtech.net/'
        self.params = {'randomId': random.uniform(1, 10)}
        #self.auth = 'Basic ZnJpZW5kbHl1c2VyOiFIQTJyVXBf'

#