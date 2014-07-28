# tom hensel <tom@jitter.eu> for CIPHRON [http://ciphron.de/]

from load_test import LoadTest

class Transaction(LoadTest):
    def __init__(self):
        self.custom_timers = {}

        # configuration
        self.test_id = 'mib-jira_https'
        self.http_url = 'https://mib-jira.iavtech.net/'
        self.http_headers = {'User-Agent': 'Mozilla/4.0 (compatible; Testing)'}
        self.http_timeout = 5
        self.http_max_redirects = 10
        self.https_verify_cert = False
