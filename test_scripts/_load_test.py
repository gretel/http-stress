# 2014 - tom hensel <tom@jitter.eu> for CIPHRON [http://ciphron.de/]

import sys
import time
import hashlib
import requests
import ssl
from _ssl_adapter import SSLAdapter

class NotConfiguredException(Exception):
    pass

class LoadTest(object):
    def __init__(self):
        raise NotConfiguredException('you need to override the __init__ method per group script to configure this test!')

    def run(self):
        def curLatency(val):
            return round(time.time() - val, 5)

        # initialize session
        s = requests.Session()
        if hasattr(self, 'https_ssl_version'):
            # use custom HTTPAdpater
            s.mount('https://', SSLAdapter(ssl_version=self.https_ssl_version))
        if hasattr(self, 'https_verify_cert'):
            # set verification of server cert
            s.verify = self.https_verify_cert
        if hasattr(self, 'http_max_redirects'):
            # set maximum number of http redirects
            s.max_redirects = self.http_max_redirects
        if hasattr(self, 'http_headers'):
            # set http header(s)
            s.headers = self.http_headers
        if hasattr(self, 'http_params'):
            # set http query parameter(s)
            http_params = self.http_params

        try:
            # store point in time
            start_timer = time.time()
            # send client certificate?
            if hasattr(self, 'https_client_cert'):
                using_cert = True # TODO get protocol from request?
                r = s.get(self.http_url, timeout=self.http_timeout, params=http_params, cert=self.https_client_cert)
            else:
                using_cert = False # TODO get protocol from request?
                r = s.get(self.http_url, timeout=self.http_timeout, params=http_params)
        except:
            # get exception info, ignore traceback
            exc_type, exc_value = sys.exc_info()[:2]
            name = exc_type.__name__
            # store latency
            latency = curLatency(start_timer)
            self.custom_timers['Exception_%s' % name] = latency
            self.logger.info('%s: %s', name , exc_value)
            # bail out
            return

        # store latency
        self.custom_timers['Response_%s' % r.status_code] = curLatency(start_timer)
        self.custom_timers['Response_RequestsLib_%s' % r.status_code] = round(r.elapsed.microseconds / 1e6, 5)

        # initialize (do not fail logging)
        hsh = ''
        # expect status code (i.e. '200')
        if r.status_code == self.http_code_ok:
            # assert string in content
            if hasattr(self, 'assert_string'):
                assert (self.assert_string in r.text), 'Assertion Failed, Expected Text: %s' % self.assert_string

            # and more specific, assert hash of content
            if hasattr(self, 'assert_hash'):
                # calculate hash
                hsh = hashlib.sha224(r.text).hexdigest()
                self.logger.debug('[%s] (Hash) %s', r.url, hsh)

                # assertion
                assert (self.assert_hash == hsh), 'Assertion Failed, Expected Hash: %s, Got Hash: %s' % (self.assert_hash, hsh)
        else:
            # if statement did not match, so status code is other than expected
            assert (True), 'Assertion Failed, Expected HTTP Code: %s, Got Code: %s' % (self.http_code_ok, r.status_code)

        # logging
        self.logger.info('[%s] (Cert: %s) -> Status: %d/%s (Expected: %s) => Duration: %.5f secs/%d bytes (Headers: %s)', r.url, using_cert, r.status_code, r.reason, self.http_code_ok, curLatency(start_timer), len(r.text), r.headers)
