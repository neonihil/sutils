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


from .primitives import qlist, qdict

__all__ = qlist()

# ---------------------------------------------------
# MetaSubclassRegister
# ---------------------------------------------------

class MetaSubclassRegister(type):

    def __new__(mcs, name, bases, fields):
        cls = super().__new__(mcs, name, bases, fields)
        for base in bases:
            register_subclass = getattr(base, '_register_subclass', None)
            if not register_subclass or register_subclass.__class__ == cls: continue
            register_subclass(cls)
        return cls


# ---------------------------------------------------
# MetaMergedDefaultOptions
# ---------------------------------------------------

class MetaMergedDefaultOptions(type):

    def __new__(mcs, name, bases, fields ):
        # print "\MetaMergedDefaultOptions.__new__", name, bases, fields
        __default_options__ = qdict()
        for base in reversed(bases):
            # print "\MetaMergedDefaultOptions.__new__", "1111", base, __default_options__
            __default_options__.update(getattr(base, '__default_options__', {}), True, True, True)
            # print "\MetaMergedDefaultOptions.__new__", "2222", base, __default_options__
        # print "\MetaMergedDefaultOptions.__new__", "3333", __default_options__
        __default_options__.update(fields.get('__default_options__', {}), True, True, True)
        # print "\MetaMergedDefaultOptions.__new__", "4444", __default_options__
        fields['__default_options__'] = __default_options__
        return super(MetaMergedDefaultOptions,mcs).__new__(mcs, name, bases, fields)


# ---------------------------------------------------
# MergedDefaultOptions
# ---------------------------------------------------

@__all__.register
class MergedDefaultOptions(object):

    __default_options__ = {}
    __default_options_check_unused__ = True
    __default_options_pop_used = True

    __metaclass__ = MetaMergedDefaultOptions

    def __init__(self, *args, **kwargs):
        # print "\n", "MergedDefaultOptions.__init__", "1111", "kwargs", kwargs
        options = qdict()
        options.update(self.__default_options__, True, convert_to_qdict = True)
        # print "\n", "MergedDefaultOptions.__init__", "2222", "after update default", options
        options.update(kwargs, True, convert_to_qdict = True)
        # print "\n", "MergedDefaultOptions.__init__", "3333", "after update kwargs", options
        for name in self.__default_options__:
            setattr(self, name, options[name])
        if self.__default_options_check_unused__:
            unused_keys = list(set(kwargs.keys()) - set(self.__default_options__.keys()))
            if len(unused_keys) > 0:
                raise TypeError("invalid keyword arguments: " + str(unused_keys))
        if self.__default_options_pop_used:
            for name in self.__default_options__:
                if name in kwargs: del kwargs[name]
        # print "\n", "MergedDefaultOptions.__init__", "4444", "after popping", kwargs
        # print "anyadbuzi!!!!", args, kwargs, self.__default_options_check_unused__, unused_keys
        super(MergedDefaultOptions,self).__init__(*args, **kwargs)



