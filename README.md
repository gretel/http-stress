## http-stress

A simple while effective HTTP and HTTPS stress testing tool that can be used to measure some types of load. It's based on [multi-mechanize](https://github.com/cgoldberg/multi-mechanize) and shares all it's benefits. While ignoring httlib2 this test makes use of the wonderful [requests](http://docs.python-requests.org/en/latest/) which utilizes httplib3 instead. Therefore, HTTPS works very well and use of client cert authentication and CA verification is possible.

**Work in progress!**

Future development intends this test to be used with [Ansible](http://ansible.com/) for remote controlled testing pleasure. Documentation is upcoming, too. Please stay tuned!

