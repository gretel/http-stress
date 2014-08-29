# 2014 - tom hensel <tom@jitter.eu> for CIPHRON [http://ciphron.de/]

import os, os.path
import sys
import random
import ssl
import logging, logging.handlers
from _load_test import LoadTest

class Transaction(LoadTest):
    def __init__(self):

# ----configuration begin ---

        # test endpoint
        self.http_url = 'https://this.might.get.flood.ed/'

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
        self.https_client_cert = './certs/client.pem'

        # verify server certificate (True/False/'cacert')
        self.https_verify_cert = './certs/cacert.pem'

        # assert string in text of response (comment out to disable)
        #self.assert_text = 'eat my cert'

        # assert hash of content in response (comment out to disable)
        #self.assert_hash = '' # todo example hash

# ----configuration end ---

        # initialize multi-mechanize
        self.custom_timers = {}

        # initialize logging facility
        logging.basicConfig(level=logging.DEBUG, format='[%(name)s] %(levelname)s: %(message)s')

        formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        logger = logging.getLogger(__name__)

        sh = logging.StreamHandler()
        logger.addHandler(sh)

        fh = logging.handlers.RotatingFileHandler('./log/%s.log' % __name__, maxBytes=327680000, backupCount=24)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info('Running on: %s, SSL Library: %s', os.uname(), ssl.OPENSSL_VERSION)

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
