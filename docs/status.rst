Status
======

Early developement stage. Implemented already:

* WSGI adapter
* HTTP standalone async-io server
* WebSockets client and server
* HTTP user agent with TLS/SSL support
* JSON pointers implementation based on :rfc:`6901`
* Embedded files loader
* HTML/XML DOM parser with CSS selectors
* URL parser with container classes for URL, path and querystring
* Non-blocking TCP client and server
* Simple logging object
* Synchronizer and sequentializer of multiple events
* Main event loop which handle IO and timer events
* Event emitter with subscriptions
* Low level event reactor based on :manpage:`select(2)` and :manpage:`poll(2)`
* Lazy properties for objects
* Test units with API based on Perl's Test::More and `TAP <http://testanything.org/>`_ protocol
