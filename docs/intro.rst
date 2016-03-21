Intro
=====

An asynchronous, event driver web framework for the Python programming language.

Pyjoyment provides own reactor which handles I/O and timer events in its own
main event loop but it supports other loops, ie. EV.

Pyjoyment uses intensively own event emmiter which should be familiar for NodeJS
programmers.

It provides tool set for parsing and creating HTTP messages and HTML documents.
It also supports WSGI interface.

Pyjoyment is compatible with Python 2.7+ and 3.3+. It doesn't require any
external libraries or compilers.

Pyjoyment is based on `Mojolicious <http://mojolicio.us>`_: a next generation
web framework for the Perl programming language.
