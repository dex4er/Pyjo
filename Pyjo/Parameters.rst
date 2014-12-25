.. highlight:: perl


################
Mojo::Parameters
################

****
NAME
****


Mojo::Parameters - Parameters


********
SYNOPSIS
********



.. code-block:: perl

   use Mojo::Parameters;
 
   # Parse
   my $params = Mojo::Parameters->new('foo=bar&baz=23');
   say $params->param('baz');
 
   # Build
   my $params = Mojo::Parameters->new(foo => 'bar', baz => 23);
   push @$params, i => '♥ mojolicious';
   say "$params";



***********
DESCRIPTION
***********


`Mojo::Parameters <http://search.cpan.org/search?query=Mojo%3a%3aParameters&mode=module>`_ is a container for form parameters used by `Mojo::URL <http://search.cpan.org/search?query=Mojo%3a%3aURL&mode=module>`_
and based on RFC 3986|http://tools.ietf.org/html/rfc3986 as well as the
HTML Living Standard|https://html.spec.whatwg.org.


**********
ATTRIBUTES
**********


`Mojo::Parameters <http://search.cpan.org/search?query=Mojo%3a%3aParameters&mode=module>`_ implements the following attributes.

charset
=======



.. code-block:: perl

   my $charset = $params->charset;
   $params     = $params->charset('UTF-8');


Charset used for encoding and decoding parameters, defaults to \ ``UTF-8``\ .


.. code-block:: perl

   # Disable encoding and decoding
   $params->charset(undef);




*******
METHODS
*******


`Mojo::Parameters <http://search.cpan.org/search?query=Mojo%3a%3aParameters&mode=module>`_ inherits all methods from `Mojo::Base <http://search.cpan.org/search?query=Mojo%3a%3aBase&mode=module>`_ and implements the
following new ones.

append
======



.. code-block:: perl

   $params = $params->append(foo => 'ba&r');
   $params = $params->append(foo => ['ba&r', 'baz']);
   $params = $params->append(foo => ['bar', 'baz'], bar => 23);


Append parameters. Note that this method will normalize the parameters.


.. code-block:: perl

   # "foo=bar&foo=baz"
   Mojo::Parameters->new('foo=bar')->append(foo => 'baz');
 
   # "foo=bar&foo=baz&foo=yada"
   Mojo::Parameters->new('foo=bar')->append(foo => ['baz', 'yada']);
 
   # "foo=bar&foo=baz&foo=yada&bar=23"
   Mojo::Parameters->new('foo=bar')->append(foo => ['baz', 'yada'], bar => 23);



clone
=====



.. code-block:: perl

   my $params2 = $params->clone;


Clone parameters.


every_param
===========



.. code-block:: perl

   my $values = $params->every_param('foo');


Similar to `param`_, but returns all values sharing the same name as an
array reference. Note that this method will normalize the parameters.


.. code-block:: perl

   # Get first value
   say $params->every_param('foo')->[0];



merge
=====



.. code-block:: perl

   $params = $params->merge(Mojo::Parameters->new(foo => 'b&ar', baz => 23));


Merge `Mojo::Parameters <http://search.cpan.org/search?query=Mojo%3a%3aParameters&mode=module>`_ objects. Note that this method will normalize the
parameters.


.. code-block:: perl

   # "foo=bar&foo=baz"
   Mojo::Parameters->new('foo=bar')->merge(Mojo::Parameters->new('foo=baz'));



new
===



.. code-block:: perl

   my $params = Mojo::Parameters->new;
   my $params = Mojo::Parameters->new('foo=b%3Bar&baz=23');
   my $params = Mojo::Parameters->new(foo => 'b&ar');
   my $params = Mojo::Parameters->new(foo => ['ba&r', 'baz']);
   my $params = Mojo::Parameters->new(foo => ['bar', 'baz'], bar => 23);


Construct a new `Mojo::Parameters <http://search.cpan.org/search?query=Mojo%3a%3aParameters&mode=module>`_ object and `parse`_ parameters if
necessary.


param
=====



.. code-block:: perl

   my @names       = $params->param;
   my $value       = $params->param('foo');
   my ($foo, $bar) = $params->param(['foo', 'bar']);
   $params         = $params->param(foo => 'ba&r');
   $params         = $params->param(foo => qw(ba&r baz));
   $params         = $params->param(foo => ['ba;r', 'baz']);


Access parameter values. If there are multiple values sharing the same name,
and you want to access more than just the last one, you can use
`every_param`_. Note that this method will normalize the parameters.


params
======



.. code-block:: perl

   my $array = $params->params;
   $params   = $params->params([foo => 'b&ar', baz => 23]);


Parsed parameters. Note that this method will normalize the parameters.


parse
=====



.. code-block:: perl

   $params = $params->parse('foo=b%3Bar&baz=23');


Parse parameters.


remove
======



.. code-block:: perl

   $params = $params->remove('foo');


Remove parameters. Note that this method will normalize the parameters.


.. code-block:: perl

   # "bar=yada"
   Mojo::Parameters->new('foo=bar&foo=baz&bar=yada')->remove('foo');



to_hash
=======



.. code-block:: perl

   my $hash = $params->to_hash;


Turn parameters into a hash reference. Note that this method will normalize
the parameters.


.. code-block:: perl

   # "baz"
   Mojo::Parameters->new('foo=bar&foo=baz')->to_hash->{foo}[1];



to_string
=========



.. code-block:: perl

   my $str = $params->to_string;


Turn parameters into a string.



*********
OPERATORS
*********


`Mojo::Parameters <http://search.cpan.org/search?query=Mojo%3a%3aParameters&mode=module>`_ overloads the following operators.

array
=====



.. code-block:: perl

   my @params = @$params;


Alias for `params`_. Note that this will normalize the parameters.


.. code-block:: perl

   say $params->[0];
   say for @$params;



bool
====



.. code-block:: perl

   my $bool = !!$params;


Always true.


stringify
=========



.. code-block:: perl

   my $str = "$params";


Alias for `to_string`_.



********
SEE ALSO
********


Mojolicious, `Mojolicious::Guides <http://search.cpan.org/search?query=Mojolicious%3a%3aGuides&mode=module>`_, `http://mojolicio.us <http://mojolicio.us>`_.

