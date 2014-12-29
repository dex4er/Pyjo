Intro
=====

Pyjo is based on Mojo: a next generation web framework for the Perl programming language.

See http://mojolicio.us/


Status
======

Early developement stage. Implemented already:

* Main event loop which handle IO and timer events
* Event emitter with subscriptions
* Synchronizer and sequentializer of multiple events
* Low level event reactor based on poll(2) function or libev (pyev) library
* Non-blocking TCP client and server
* Lazy properties for objects
* URL parser
* Test units with API based on Perl's Test::More and TAP protocol
* Regexp objects with overloaded operators
