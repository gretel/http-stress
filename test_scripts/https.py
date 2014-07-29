# tom hensel <tom@jitter.eu> for CIPHRON [http://ciphron.de/]

from _load_test import LoadTest
import random
import os
import os.path

class Transaction(LoadTest):
    def __init__(self):
        # initialize multi-mechanize
        self.custom_timers = {}

# ----- configuration begin ---

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

        # client certificate (comment out to disable)
        #self.https_client_cert = './certs/client.pem'

        # verify server certificate (True/False)
        self.https_verify_cert = False

        # assert string in response tesxt (comment out to disable)
        self.assert_text = 'IAV'

# ----- configuration end ---

        # sanity check
        if hasattr(self, 'https_client_cert'):
            if os.path.isfile(self.https_client_cert) and os.access(self.https_client_cert, os.R_OK):
                print 'using client certificate: %s' % self.https_client_cert
            else:
                print 'thread aborting! unable to access client certificate: %s' % self.https_client_cert
                sys.exit(1)
