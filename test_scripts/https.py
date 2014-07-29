# tom hensel <tom@jitter.eu> for CIPHRON [http://ciphron.de/]

from _load_test import LoadTest
import random

class Transaction(LoadTest):
    def __init__(self):
        # initialize multi-mechanize
        self.custom_timers = {}

        # get random number
        self.rndm = random.uniform(1, 10)

        # configuration
        self.test_id = 'mib-jira_https'
        self.http_url = 'https://mib-jira.iavtech.net/'
        self.http_headers = {'User-Agent': 'Mozilla/4.0 (compatible; Testing)'}
        self.http_timeout = 3
        self.http_max_redirects = 3
        self.https_verify_cert = False
        # client certificate
        #self.https_client_cert = 'certs/client.pem'
