# -*- coding: utf-8 -*-

"""
Pyjo.Mixin.String - Methods for object with to_str() method
===========================================================
::

    import Pyjo.Base
    import Pyjo.Mixin.String

    class SubClass(Pyjo.Base.object, Pyjo.Mixin.String.object):
        def to_str(self):
            return 'value'

The mixin class for objects with :meth:`to_str` method.
"""


import Pyjo.Base

from Pyjo.Util import not_implemented

import platform
import sys


class Pyjo_Mixin_String(object):
    """
    This mixin does not provide own constructor method.
    """

    def __bool__(self):
        """::

            boolean = bool(obj)

        True if string representation is also true. (Python 3.x)
        """
        return bool(self.to_str())

    def __bytes__(self):
        """::

            bstring = bytes(obj)

        Byte-string representation of an object. (Python 3.x)
        """
        if hasattr(self, 'to_bytes'):
            return self.to_bytes()
        else:
            return bytes(self.to_str(), 'utf-8')

    def __complex__(self):
        """::

            complexnumber = complex(obj)

        Converts string representation into complex number.
        """
        return complex(self.to_str())

    def __eq__(self, other):
        """::

            boolean = obj == other

        True if string representation of the object is equal to other value.
        """
        return str(self) == other

    def __float__(self):
        """::

            floatnumber = float(self)

        Converts string representation into float number.
        """
        return float(self.to_str())

    def __ge__(self, other):
        """::

            boolean = obj >= other

        True if string representation of the object is equal or greater than other value.
        """
        return str(self) >= other

    def __gt__(self, other):
        """::

            boolean = obj > other

        True if string representation of the object is greater than other value.
        """
        return str(self) > other

    def __hash__(self):
        """::

            hashvalue = hash(obj)

        Returns hash value of string representation of this object.
        """
        return hash(self.to_str())

    def __hex__(self):
        """::

            hexnumber = hex(self)

        Converts string representation into hexadecimal number.
        """
        return hex(int(self.to_str()))

    if platform.python_implementation() != 'PyPy' or sys.version_info < (3, 0):
        def __int__(self):
            """::

                intnumber = int(obj)

            Converts string representation into integer number.
            """
            return int(self.to_str())
    else:
        pass  # PyPy3 error

    def __le__(self, other):
        """::

            boolean = obj <= other

        True if string representation of the object is equal or lesser than other value.
        """
        return str(self) <= other

    def __long__(self):
        """::

            longnumber = long(obj)

        Converts string representation into long number.
        """
        return long(self.to_str())

    def __lt__(self, other):
        """::

            boolean = obj < other

        True if string representation of the object is lesser than other value.
        """
        return str(self) < other

    def __ne__(self, other):
        """::

            boolean = obj != other

        True if string representation of the object is not equal to other value.
        """
        return str(self) != other

    def __nonzero__(self):
        """::

            boolean = bool(obj)

        True if string representation is also true. (Python 2.x)
        """
        return bool(self.to_str())

    def __oct__(self):
        """::

            octnumber = oct(obj)

        Converts string representation into octadecimal number.
        """
        return oct(int(self.to_str()))

    def __repr__(self):
        """::

            reprstring = repr(obj)

        String representation of an object shown in console.
        """
        if self.__module__ == '__main__':
            return "{0}('{1}')".format(self.__class__.__name__, str(self))
        elif isinstance(self, Pyjo.Base.object):
            return "{0}.new('{1}')".format(self.__module__, str(self))
        else:
            return "{0}.{1}('{2}')".format(self.__module__, self.__class__.__name__, str(self))

    def __str__(self):
        """::

            string = str(obj)

        String representation of an object.
        """
        string = self.to_str()
        if string is None:
            string = 'None'
        return string

    def __unicode__(self):
        """::

            ustring = unicode(obj)

        Unicode-string representation of an object. (Python 2.x)
        """
        return unicode(self.to_str())

    @not_implemented
    def to_str(self):
        """
        Needs to be implemented in subclass.
        """
        pass


object = Pyjo_Mixin_String  # @ReservedAssignment
