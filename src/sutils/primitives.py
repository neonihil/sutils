#!/usr/bin/env python
# project: sutils
# description: Smart Utilities
# file: sutils/sutils.py
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

import weakref
import re
import types


# ---------------------------------------------------
# qlist
# ---------------------------------------------------

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


# ---------------------------------------------------
# __all__
# ---------------------------------------------------

__all__ = qlist()
__all__.register(qlist)

# ---------------------------------------------------
# qdict
# ---------------------------------------------------

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
        self[key] = value        

    def copy( self, add = None ):
        res = qdict()
        res.update( self )
        if add:
            res.update( add )
        return res
        
    def __add__( self, other ):
        res = self.copy()
        res.update( other )
        return res

    def update( self, source, recursive = False, add_keys = True ):
        if not isinstance(source, dict): return
        if not recursive:
            if add_keys:
                return super(qdict,self).update(source)
            for k in self:
                self[k] = source.get(k,self[k])
            return
        if add_keys:
            for k, nv in source.iteritems():
                if k in self:
                    cv = self[k]
                    if isinstance(cv, qdict):
                        cv.update(nv, recursive = recursive, add_keys = add_keys)
                        continue
                    elif isinstance(cv, dict):
                        cv.update(nv)
                        continue
                self[k] = nv
            return
        for k, cv in self.iteritems():
            try:
                nv = source[k]
            except KeyError:
                continue
            if isinstance(cv, qdict):
                cv.update(nv, recursive = recursive, add_keys = add_keys)
            elif isinstance(cv, dict):
                cv.update(nv)
            else:
                self[k] = nv


# -------------------------------------------------------------------------------
# SmartEnum
# -------------------------------------------------------------------------------

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

except ImportError:
    @__all__.register
    class SmartEnum(object):
        class __metaclass__(type):
            def __new__(mcs, name, bases, fields):
                if name == 'SmartEnum': return type.__new__(mcs,name,bases,fields)
                raise ImportError('Failed to import Enum. Under python27 please use pip install enum34.')


# ---------------------------------------------------
# @weakproperty
# ---------------------------------------------------

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


# ---------------------------------------------------
# cachedproperty
# ---------------------------------------------------    

@__all__.register
def cachedproperty( *args, **kwargs ):
    """Creates a cached property (only set one)
    """
    def _cachedproperty( func ):
        varname = '_' + func.func_name
        def getter(self):
            value = getattr( self, varname, None)
            if value is None:
                value = func(self, *args, **kwargs )
                setattr( self, varname, value )
            return value
        def setter(self, value):
            setattr(self, varname, value)
        def deleter(self):
            setattr(self, varname, None)
        return property( getter, setter, deleter )
    if (len(args) >= 1) and isinstance( args[0], types.FunctionType ):
        func, args = args[0], args[1:]
        return _cachedproperty( func )
    return _cachedproperty

