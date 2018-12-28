#!/usr/bin/env python
# project: sutils
# description: Smart Utilities
# file: sutils/primitives.py
# file-version: 3.1
# author: DANA <dkovacs@deasys.eu>
# license: GPL 3.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# -----------------------------------------------------------------------------
# imports
# -----------------------------------------------------------------------------

import sys
import weakref
import types


# -----------------------------------------------------------------------------
# PYTHON3
# -----------------------------------------------------------------------------

_PYTHON3 = True if sys.version_info[0] >= 3 else False


# -----------------------------------------------------------------------------
# qlist
# -----------------------------------------------------------------------------

class qlist(list):
    """Quick Enhanced List
    """

    def get( self, index, default = None ):
        if (index < 0) or ( index >= len(self) ):
            return default
        return self[index]
        
    def register( self, item ):
        self.append( item.__name__ )
        return item

    def __str__(self):
        return '[' + ', '.join([str(i) for i in self]) + ']'


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()
__all__.register(qlist)


# ---------------------------------------------------------------------------------------------------------
# NA
# ---------------------------------------------------------------------------------------------------------

class NAMeta(type):
    __repr__ = lambda s: "NA"
    __str__ = lambda s: "??"

class _NA(object):
    """This class represents the 'Not Available' value. 

    Can be usefull when a need to return that there is no value for the function,
    but None is also considered as a meaningfull value.

    """
        
    __repr__ = lambda s: "NA"
    __str__ = lambda s: "??"

    def __eq__(self, other):
        if isinstance(other,NA):
            return True
        if isinstance(other, type) and issubclass(other,NA):
            return True
        return False

NA = NAMeta("NA", (_NA,), {})

__all__.append("NA")


# -----------------------------------------------------------------------------
# qdict
# -----------------------------------------------------------------------------

@__all__.register
class qdict(dict):
    """Simple Attribute Dictionary
    
    Usage::
        
        >>> d = qdict( a = 'some', b = 'thing' )
        >>> d
        { 'a': 'some', 'b': 'thing' }
        >>> d.a
        'some'
        >>> d.c = 1235
        >>> d
        { 'a': 'some', 'b': 'thing', 'c': 1235 }
    
    """
    def __init__(self, *args, **kw):
        super(qdict,self).__init__( *args, **kw )

    def __getattr__(self, key):
        if not key in self:
            raise AttributeError(key)
        return self[key]

    def __setattr__(self, key, value):
        if key.startswith('_') or key in self.__dict__ or key in self.__class__.__dict__:
            return super(qdict, self).__setattr__(key, value)
        self[key] = value

    def copy( self, add = None ):
        res = qdict()
        res.update( self, False )
        if add:
            res.update( add )
        return res
        
    def __add__( self, other ):
        res = self.copy()
        res.update( other )
        return res

    def update( self, source, recursive = False, add_keys = True, convert_to_qdict = False ):
        # print ">> self: ", self
        # print "\n>> source: ", source
        # print "\n>> recursive: ", recursive
        # print ">> add_keys: ", add_keys
        # print ">> convert_to_qdict: ", convert_to_qdict
        if not isinstance(source, dict): return self
        if not recursive:
            if add_keys:
                super(qdict,self).update(source)
                return self
            for k in self:
                self[k] = source.get(k,self[k])
            return self
        if add_keys:
            for k, nv in source.items():
                if convert_to_qdict and isinstance(nv, dict) and (not isinstance(nv, qdict)):
                    nv_ = qdict()
                    nv_.update(nv, recursive = recursive, add_keys = add_keys, convert_to_qdict = convert_to_qdict)
                    nv = nv_
                if isinstance(nv, dict) and (k in self):
                    cv = self[k]
                    if isinstance(cv, dict) and convert_to_qdict:
                        cv = qdict(cv)
                        self[k] = cv
                    if isinstance(cv, qdict):
                        cv.update(nv, recursive = recursive, add_keys = add_keys, convert_to_qdict = convert_to_qdict)
                        continue
                    if isinstance(cv, dict):
                        cv.update(nv)
                        continue
                if convert_to_qdict and isinstance(nv, list):
                    for i in range(len(nv)):
                        if isinstance(nv[i], qdict): continue
                        if isinstance(nv[i], dict):
                            nnv = qdict()
                            nnv.update(nv[i], True, add_keys, convert_to_qdict)
                            nv[i] = nnv
                self[k] = nv
            return self
        for k, cv in self.items():
            try:
                nv = source[k]
                if convert_to_qdict and isinstance(nv, dict) and (not isinstance(nv, qdict)):
                    nv_ = qdict()
                    nv_.update(nv, recursive = recursive, add_keys = add_keys, convert_to_qdict = convert_to_qdict)
                    nv = nv_
            except KeyError:
                continue
            if isinstance(cv, qdict):
                cv.update(nv, recursive = recursive, add_keys = add_keys)
            elif isinstance(cv, dict):
                cv.update(nv)
            else:
                self[k] = nv
        return self


    def update__( self, *a, **kw):
        # print "\n\n---------->> qdict.update", "0000", id(self)
        self.update2(*a, **kw)
        # print "---------->> qdict.update", "1111", id(self), "\n\n", self, "\n", "-" * 100, "\n\n"
        return self


# -----------------------------------------------------------------------------
# ObjectDict
# -----------------------------------------------------------------------------

@__all__.register
class ObjectDict(qdict):

    def register(self, *args):
        if len(args) == 1 and hasattr(args[0], '__name__'):
            self[args[0].__name__] = args[0]
            return args[0]
        name = args[0]
        def _register(obj):
            self[name] = obj
            return obj
        return _register

    def register_module(self, module):
        for name in dir(module):
            value = getattr(module, name)
            if isinstance(value, type):
                self.register(value)


# ---------------------------------------------------------------------------------------------------------
# SmartEnum
# ---------------------------------------------------------------------------------------------------------

try:
    from enum import Enum

    @__all__.register
    class SmartEnum(Enum):
        """SmartEnum - Enumeration Extended
        """

        @classmethod
        def keys(cls):
            return [ str(i.name) for i in cls]

        @classmethod
        def values(cls):
            return [ str(i.value) for i in cls]

        # def __cmp__(self, other):
        #     return str(self) < str(other)

except ImportError:
    @__all__.register
    class SmartEnum(object):
        class __metaclass__(type):
            def __new__(mcs, name, bases, fields):
                if name == 'SmartEnum': return type.__new__(mcs,name,bases,fields)
                raise ImportError('Failed to import Enum. Under python27 please use pip install enum34.')


# -----------------------------------------------------------------------------
# @weakproperty
# -----------------------------------------------------------------------------

@__all__.register
def weakproperty( obj ):
    """Use @property, but it creates a weak reference property for the given name.
    
    Usage::
        
        class A(object):
            @weakproperty
            def myprop(): 
                print "property changed"
    
        obj = A()           # Create instance of A
        obj.myprop = obj    # Set the property to reference to itself
        del obj             # This will free obj, becouse myprop is weak and no circular references are made.
        
    """
    name = obj.__name__
    def getter(self):
        value = getattr(self, "_" + name, None )
        return value() if isinstance(value, weakref.ref) else value
    def setter( self, value ):
        ref = weakref.ref( value ) if value is not None else None
        setattr( self, '_' + name, ref )
        obj( self, value )     
    return property(getter, setter)


# -----------------------------------------------------------------------------
# cachedproperty
# -----------------------------------------------------------------------------    

@__all__.register
def cachedproperty(getter_ = None, setter = None, deleter = None, varname = None):
    """Creates a cached property (only set one)
    """
    varname_ = varname
    def _cachedproperty(getter):
        varname = varname_ or ('_' + getattr(getter, "__name__" if _PYTHON3 else "func_name"))
        def _getter(self):
            value = getattr( self, varname, None)
            if value is None:
                value = getter(self)
                setattr( self, varname, value )
            return value
        def _setter(self, value):
            setattr(self, varname, value)
        def _deleter(self):
            setattr(self, varname, None)
        return property( _getter, setter or _setter, deleter or _deleter )
    # if (len(args) >= 1) and isinstance( args[0], types.FunctionType ):
    #     func, args = args[0], args[1:]
    #     return _cachedproperty( func )
    if getter_:
        return _cachedproperty(getter_)
    return _cachedproperty



# -----------------------------------------------------------------------------
# PrettyObject
# -----------------------------------------------------------------------------    

@__all__.register
class PrettyObject(object):

    def __str__(self):
        return repr(self)

    @classmethod
    def get_pretty_fields(cls):
        if not getattr(cls, '__pretty_field_format__', None):
            fields = getattr(cls, '__pretty_fields__', None )
            if not fields:
                fields = getattr(cls, '__slots__', None )            
            if not fields:
                cls.__pretty_field_format__ = False
            cls.__pretty_field_format__ = ', '.join([ "{0}={{{0}}}".format(n) for n in fields ])
        return cls.__pretty_field_format__


    def __repr__(self):
        result = super(PrettyObject,self).__repr__()
        fields = getattr(self.__class__, '__pretty_fields__', None )
        if fields is None:
            fields = getattr(self.__class__, '__slots__', None )
        if fields:
            context = {}
            for name in fields:
                try:
                    value = repr(getattr(self,name,NA))
                except Exception as exc:
                    value = exc
                context[name] = value
            result = result[:-1] + ' '
            result += self.get_pretty_fields().format(**context) + '>'
        return result

