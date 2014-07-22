import hashlib
import time
import urllib2

class Transaction(object):
    def __init__(self):
        self.custom_timers = {}

    def run(self):
        # id of testcase
        test_id = 'www.iav.com_ssl'

        # request timeout
        http_timeout = 10

        # http server to profile
        url = 'https://www.iav.com/'


        # initialize urllib
        req = urllib2.Request(url = url)

        # set 'User-Agent' header
        user_agent = 'Mozilla/4.0 (compatible; Testing)'
        req.add_header('User-Agent', user_agent)

        # set 'Authorization' header
#        auth = 'Basic ZnJpZW5kbHl1c2VyOiFIQTJyVXBf'
#        req.add_header('Authorization', auth)

        # start measurement
        start_timer = time.time()

        # send request, get response
        response = urllib2.urlopen(req, timeout = http_timeout)

        # retrieve content (which adds a bit of delay, too)
        content = response.read().strip()

        # stop measurement
        latency = time.time() - start_timer

        # verbose info
        print 'url:', response.geturl(), ', code:', response.code, ', hash:', hashlib.sha224(content).hexdigest()

        # store latency
        self.custom_timers[test_id] = latency

        # asset response code of 200 (HTTP OK)
        assert (response.code == 200), 'Bad Response: HTTP %s' % response.code

        # assert known string in content
        #assert ('iav' in content), 'Text Assertion Failed'
