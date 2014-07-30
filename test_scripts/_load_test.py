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
        # initialize session
        s = requests.Session()

        if hasattr(self, 'http_max_redirects'):
            s.max_redirects = self.http_max_redirects
        if hasattr(self, 'http_headers'):
            s.headers = self.http_headers
        if hasattr(self, 'http_params'):
            http_params = self.http_params
        if hasattr(self, 'https_verify_cert'):
            s.verify = self.https_verify_cert

        # start measurement
        start_timer = time.time()

        try:
            if hasattr(self, 'https_client_cert'):
                using_cert = True # todo get protocol from request?
                r = s.get(self.http_url, timeout=self.http_timeout, params=http_params, cert=self.https_client_cert)
            else:
                using_cert = False # todo get protocol from request?
                r = s.get(self.http_url, timeout=self.http_timeout, params=http_params)
        except requests.exceptions.RequestException as e:
            print '[RequestException] %s' % e

        # stop measurement
        latency = time.time() - start_timer

        # store latency
        self.custom_timers['Got_Response'] = latency

        # initialize (do not fail logging)
        hsh = ''

        # expect status code (i.e. '200')
        if r.status_code == self.http_code_ok:
            # ok, calculate hash of content in response
            hsh = hashlib.sha224(r.content).hexdigest()

            # done hashing (this took some time and adds some delay)
            self.custom_timers['Got_Content_Locally'] = time.time() - start_timer

            # assert string in content
            if hasattr(self, 'assert_string'):
                assert (self.assert_string in r.content), 'Assertion Failed, Expected Text: %s' % self.assert_string

            # and more specific, assert hash of content
            if hasattr(self, 'assert_hash'):
                assert (self.assert_hash == hsh), 'Assertion Failed, Expected Hash: %s, Got Hash: %s' % (self.assert_hash, hsh)
        else:
            # if statement did not match, so status code is other than expected
            assert (True), 'Assertion Failed, Expected HTTP Code: %s, Got Code: %s' % (self.http_code_ok, r.status_code)

        print '[%s] (cert: %s) -> %d/%s => %.5f secs (%s)' % (r.url, using_cert, r.status_code, r.reason, latency, hsh)
