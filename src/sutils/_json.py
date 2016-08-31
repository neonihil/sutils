#!/usr/bin/env python
# project: sutils
# description: Smart Utilities
# file: sutils/json.py
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


# ---------------------------------------------------
# imports
# ---------------------------------------------------    

import json as _json

from .primitives import qdict, qlist


# ---------------------------------------------------
# exports
# ---------------------------------------------------    

__all__ = qlist()


# ---------------------------------------------------
# extended_encoder
# ---------------------------------------------------    

# def extended_encoder( obj ):
#     if isinstance(obj, datetime.datetime):
#         return obj.isoformat()
#     if isinstance(obj, Exception):
#         d = __dict__ = getattr( obj, '__dict__', {} )
#         d.update( { 'message': obj.message } )
#         return qdict( __class__ = obj.__class__.__module__ + '.' + obj.__class__.__name__, __dict__ = d )
#     if isinstance(obj, object):
#         return qdict( __class__ = obj.__class__.__module__ + '.' + obj.__class__.__name__, __dict__ = getattr( obj, '__dict__', None ) )
#         return dict( filter(  )
#     else:
#         raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % ( type(obj), repr(obj) )


# ---------------------------------------------------
# extended_decoder
# ---------------------------------------------------    
    
def extended_decoder( obj ):
    return qdict( **obj )


# ---------------------------------------------------
# load
# ---------------------------------------------------    

@__all__.register
def load( *args, **kwargs ):
    kwargs.setdefault( 'object_hook', extended_decoder )
    return _json.load( *args, **kwargs )


# ---------------------------------------------------
# loads
# ---------------------------------------------------    

@__all__.register
def loads( *args, **kwargs ):
    kwargs.setdefault( 'object_hook', extended_decoder )
    return _json.loads( *args, **kwargs )


# ---------------------------------------------------
# dump
# ---------------------------------------------------    

@__all__.register
def dump( *args, **kwargs ):
    # kwargs.setdefault( 'default', extended_encoder )
    return _json.dump( *args, **kwargs )

# ---------------------------------------------------
# dumps
# ---------------------------------------------------    

@__all__.register
def dumps( *args, **kwargs ):
    # kwargs.setdefault( 'default', extended_encoder )
    return _json.dumps( *args, **kwargs )



