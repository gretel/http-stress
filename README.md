## http-stress

A simple while effective HTTP and HTTPS stress testing tool that can be used to measure some types of load. It's solely based on [multi-mechanize](https://github.com/cgoldberg/multi-mechanize) and shares all of it's benefits. While ignoring httlib2 this test makes use of the wonderful [requests](http://docs.python-requests.org/en/latest/) library which utilizes httplib3. Therefore, HTTPS works very well and cert-based authentication and CA-verification is possible.

A [hackish fork of multi-mechanize](https://github.com/gretel/multi-mechanize) hard-removes the dependency on [matplotlib](http://matplotlib.org/) which can be a hassle to install on some platforms (like [OpenBSD 5.5](http://www.openbsd.org/) which this code has been developed on).

**Work in progress!**

Future development intends this test to be used with [Ansible](http://ansible.com/) for remote controlled testing pleasure. Documentation is upcoming, too. Please stay tuned!

