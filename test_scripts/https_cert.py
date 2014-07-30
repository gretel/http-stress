# 2014 - tom hensel <tom@jitter.eu> for CIPHRON [http://ciphron.de/]

import os, os.path
import sys
import logging
import random
import ssl
from _load_test import LoadTest

class Transaction(LoadTest):
    def __init__(self):
        # initialize multi-mechanize
        self.custom_timers = {}

        # initialize logging facility
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
        self.logger = logging.getLogger(__name__)
        self.logger.info('[%s] Running on: %s, SSL Library: %s', __name__, os.uname(), ssl.OPENSSL_VERSION)

# ----configuration begin ---

        # test endpoint
        self.http_url = 'https://mib-jira.iavtech.net/'

        # http timeout
        self.http_timeout = 3

        # maximum allowed redirects
        self.http_max_redirects = 3

        # positive http response code
        self.http_code_ok = 200

        # http headers to send (disable = {})
        self.http_headers = {'User-Agent': 'Mozilla/4.0 (compatible; Testing)'}

        # query parameters (disable = {})
        self.http_params = {'rndm': random.uniform(1, 10)}

        # verify server certificate (ssl.PROTOCOL_SSLv2,ssl.PROTOCOL_SSLv23,ssl.PROTOCOL_SSLv3,ssl.PROTOCOL_TLSv1)
        self.https_ssl_version = ssl.PROTOCOL_TLSv1

        # client certificate (comment out to disable)
        #self.https_client_cert = './certs/client.pem'

        # verify server certificate (True/False/'cacert')
        #self.https_verify_cert = './certs/cacert.pem'

        # assert string in text of response (comment out to disable)
        #self.assert_text = 'IAV'

        # assert hash of content in response (comment out to disable)
        #self.assert_hash = '3949234982374982374982374' # todo example hash

# ----configuration end ---

        # sanity check
        if hasattr(self, 'https_client_cert'):
            if os.path.isfile(self.https_client_cert) and os.access(self.https_client_cert, os.R_OK):
                pass
            else:
                self.logger.critical('thread aborting! unable to access client certificate: %s', self.https_client_cert)
                sys.exit(1)

        # sanity check
        if hasattr(self, 'https_verify_cert') and type(self.https_verify_cert) is not bool:
            if os.path.isfile(self.https_verify_cert) and os.access(self.https_verify_cert, os.R_OK):
                pass
            else:
                self.logger.critical('thread aborting! unable to access CA certificate: %s', self.https_verify_cert)
                sys.exit(1)
