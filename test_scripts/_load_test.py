# tom hensel <tom@jitter.eu> for CIPHRON [http://ciphron.de/]

import requests
import hashlib
import time

class NotConfiguredException(Exception):
    pass

class LoadTest(object):
    def __init__(self):
        raise NotConfiguredException('you need to override the __init__ method per group script to configure this test!')

    def run(self):
        # start measurement
        start_timer = time.time()

        # initialize session
        s = requests.Session()
        s.max_redirects = self.http_max_redirects
        s.headers = self.http_headers
        s.verify = self.https_verify_cert

        # set query parameters
        http_params = {'rndm': self.rndm}

        # do request
        if hasattr(self, 'https_client_cert'):
            r = s.get(self.http_url, timeout=self.http_timeout, params=http_params, cert=self.https_client_cert)
        else:
            r = s.get(self.http_url, timeout=self.http_timeout, params=http_params)

        # stop measurement
        latency = time.time() - start_timer

        # store latency
        self.custom_timers[self.test_id] = latency

        # verbose output
        #print 'id -> ', self.test_id, ', url:', r.url, ', code:', r.status_code, ', reason:', r.reason, ', elapsed:', r.elapsed, 'hash:', hashlib.sha224(r.text).hexdigest()

        # asset response code of 200 (HTTP OK)
        assert (r.status_code == requests.codes.ok), 'Bad Response: HTTP Code %s' % r.status_code

        # assert known string in content
        #assert ('iav' in content), 'Text Assertion Failed'

#