# tom hensel <tom@jitter.eu> for CIPHRON [http://ciphron.de/]

import time
import requests
import hashlib

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
        http_params = self.http_params

        try:
            if hasattr(self, 'https_client_cert'):
                using_cert = True
                r = s.get(self.http_url, timeout=self.http_timeout, params=http_params, cert=self.https_client_cert)
            else:
                using_cert = False
                r = s.get(self.http_url, timeout=self.http_timeout, params=http_params)
        except requests.exceptions.RequestException as e:
            print '[RequestException] %s' % e

        # stop measurement
        latency = time.time() - start_timer

        # store latency
        self.custom_timers[r.status_code] = latency

        # verbose output
        print '[%s] (cert: %s) -> %d/%s => %.5f secs (%s)' % (r.url, using_cert, r.status_code, r.reason, latency, hashlib.sha224(r.text).hexdigest())

        if r.status_code == self.http_code_ok:
            if hasattr(self, 'assert_string'):
                assert (self.assert_string in r.content), 'Assertion Failed, Text: %s' % self.assert_string
        else:
            assert (True), 'Assertion Failed: HTTP Code: %s' % r.status_code
