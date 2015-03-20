Status
======

Early developement stage. Implemented already:

* HTTP user agent with TLS support
* JSON pointers implementation based on :rfc:`6901`
* HTML/XML DOM parser with CSS selectors
* URL parser with container classes for URL, path and querystring
* Non-blocking TCP client and server
* Synchronizer and sequentializer of multiple events
* Main event loop which handle IO and timer events
* Event emitter with subscriptions
* Low level event reactor based on select(2) and poll(2)
* Lazy properties for objects
* Test units with API based on Perl's Test::More and `TAP <http://testanything.org/>`_ protocol
