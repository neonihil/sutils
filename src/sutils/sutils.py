#!/usr/bin/env python
# project: sutils
# description: Smart Utilities
# file: sutils/sutils.py
# file_version: 3.1
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

from threading import Thread
from Queue import Queue, Empty


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


# ---------------------------------------------------
# format_filesize()
# ---------------------------------------------------

__format_filesize_precisions = (
    ( 'bytes', 0 ),
    ( 'k', 0 ),
    ( 'M', 1 ),
    ( 'G', 2 ),
    ( 'T', 2 ),
    ( 'P', 2 ),
    ( 'E', 2 ),
)

@__all__.register
def format_filesize( size, precision = None ):
    for unit, prec in __format_filesize_precisions:
        if size < 1024.0:
            return "{:3.{prec}f} {}".format( size, unit, prec = precision or prec )
        size /= 1024.0
    return "%3.1f%s" % (num, 'EB')


# ---------------------------------------------------
# setup_logging()
# ---------------------------------------------------

logging = None

LOG_FORMATS = qdict(
    short = "%(asctime)s\t%(levelname)s\t%(name)s:\t%(message)s",
    thread = "%(asctime)s\t%(levelname)s\t[tid:%(thread)x (%(threadName)s)]\t%(name)s:\t%(message)s",
    process = "%(asctime)s\t%(levelname)s\t[pid:%(process)d]\t%(name)s:\t%(message)s",
    full = "%(asctime)s\t%(levelname)s\t[pid:%(process)d tid:%(thread)x (%(threadName)s)]\t%(name)s:\t%(message)s",
)

def setup_logging( level = 'INFO', format_ = LOG_FORMATS.short):
    global logging
    if not logging:
        import logging as logging_
        logging = logging_
    logging.basicConfig( format = format_, level = level )


# ---------------------------------------------------
# logged()
# ---------------------------------------------------

def _add_logger(obj, channel = None, root_channel = None, attr_name = "__logger" ):
    setup_logging()
    cls = obj
    channel = channel or cls.__name__
    root_channel = root_channel if root_channel is not None else cls.__module__
    if root_channel:
        channel = root_channel + '.' + channel
    if attr_name.startswith( '__' ): 
        attr_name = '_' + cls.__name__ + '__logger'
    setattr( obj, attr_name, logging.getLogger(channel) )

@__all__.register
def logged(obj):
    _add_logger(obj, root_channel = '')
    return obj


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
        def deleter(self):
            setattr(self, varname, None)
        return property( getter, None, deleter )
    if (len(args) >= 1) and isinstance( args[0], types.FunctionType ):
        func, args = args[0], args[1:]
        return _cachedproperty( func )
    return _cachedproperty


# ---------------------------------------------------
# camelize()
# ---------------------------------------------------
# origin: https://github.com/jpvanhal/inflection/blob/master/inflection.py

@__all__.register
def camelize(string, uppercase_first_letter=True):
    """
    Convert strings to CamelCase.
    Examples::
        >>> camelize("device_type")
        "DeviceType"
        >>> camelize("device_type", False)
        "deviceType"
    :func:`camelize` can be though as a inverse of :func:`underscore`, although
    there are some cases where that does not hold::
        >>> camelize(underscore("IOError"))
        "IoError"
    :param uppercase_first_letter: if set to `True` :func:`camelize` converts
        strings to UpperCamelCase. If set to `False` :func:`camelize` produces
        lowerCamelCase. Defaults to `True`.
    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]


# ---------------------------------------------------
# underscore()
# ---------------------------------------------------
# origin: https://github.com/jpvanhal/inflection/blob/master/inflection.py

@__all__.register
def underscore(word):
    """
    Make an underscored, lowercase form from the expression in the string.
    Example::
        >>> underscore("DeviceType")
        "device_type"
    As a rule of thumb you can think of :func:`underscore` as the inverse of
    :func:`camelize`, though there are cases where that does not hold::
        >>> camelize(underscore("IOError"))
        "IoError"
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


# --------------------------------------------
# firstline()
# --------------------------------------------

@__all__.register
def firstline(s):
    return s.split('\n', 1)[0] if s else ''


# ---------------------------------------------------
# UnexpectedEndOfStream
# ---------------------------------------------------

@__all__.register
class UnexpectedEndOfStream(Exception): pass


# ---------------------------------------------------
# NonBlockingStreamReader
# ---------------------------------------------------
# origin: https://gist.github.com/EyalAr/7915597#file-nbstreamreader-py

@__all__.register
class NonBlockingStreamReader(object):

    def __init__(self, stream):
        """
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        """

        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            """
            Collect lines from 'stream' and put them in 'quque'.
            """
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None

