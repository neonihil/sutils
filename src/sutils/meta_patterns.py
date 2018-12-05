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

from copy import copy, deepcopy

from .primitives import qlist, qdict


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()


# -----------------------------------------------------------------------------
# MetaSubclassRegister
# -----------------------------------------------------------------------------

class MetaSubclassRegister(type):

    def __new__(mcs, name, bases, fields):
        cls = super().__new__(mcs, name, bases, fields)
        for base in bases:
            register_subclass = getattr(base, '_register_subclass', None)
            if not register_subclass or register_subclass.__class__ == cls: continue
            register_subclass(cls)
        return cls


# -----------------------------------------------------------------------------
# MetaMergedDefaultOptions
# -----------------------------------------------------------------------------

class MetaMergedDefaultOptions(type):

    def __new__(mcs, name, bases, fields ):
        # print "\n\nMetaMergedDefaultOptions.__new__", "0000", mcs, name, bases, fields
        default_options = qdict()
        default_options_from_class = False
        for base in reversed(bases):
            # print "\nMetaMergedDefaultOptions.__new__", "1111  ----->", base, default_options
            default_options.update(getattr(base, '__default_options__', {}), True, True, True)
            default_options_from_class = default_options_from_class or getattr(base, '__default_options_from_class__', False)
            # print "\nMetaMergedDefaultOptions.__new__", "1111        ", base, default_options
        # print "\nMetaMergedDefaultOptions.__new__", "2222", default_options
        # print "\nMetaMergedDefaultOptions.__new__", "3333", fields.get('__default_options__', None)
        default_options.update(fields.get('__default_options__', {}), True, True, True)

        if default_options_from_class:
            # print "\nMetaMergedDefaultOptions.__new__", "4444", default_options
            class_defaults = {}
            for key_name in default_options.iterkeys():
                if not key_name in fields: continue
                value = fields[key_name]
                if callable(value) or isinstance(value, property): continue
                class_defaults[key_name] = fields.pop(key_name)
            default_options.update(class_defaults, True, True, False)
        # print "\nMetaMergedDefaultOptions.__new__", "5555", name, default_options
        fields['__default_options__'] = default_options
        return super(MetaMergedDefaultOptions,mcs).__new__(mcs, name, bases, fields)


# -----------------------------------------------------------------------------
# MergedDefaultOptions
# -----------------------------------------------------------------------------

@__all__.register
class MergedDefaultOptions(object):

    __default_options__ = {}
    __default_options_check_unused__ = True
    __default_options_pop_used__ = True
    __default_options_from_class__ = False

    __metaclass__ = MetaMergedDefaultOptions

    def __init__(self, *args, **kwargs):
        # print "\n\n", "MergedDefaultOptions.__init__", "0000", self.__class__, self
        # print "\n", "MergedDefaultOptions.__init__", "1111", "kwargs", kwargs
        options = qdict()
        options.update(self.__default_options__, True, convert_to_qdict = True)
        # print "\n", "MergedDefaultOptions.__init__", "2200", "after update defaults", options
        # if self.__default_options_from_class__:
        #     # print "\n", "MergedDefaultOptions.__init__", "2211", "updating with __class__.__dict__: ", self.__class__.__dict__
        #     options.update(dict(self.__class__.__dict__.items()), True, True, False)
        #     # print "\n", "MergedDefaultOptions.__init__", "2222", "after update with __class__", options
        options.update(kwargs, True, convert_to_qdict = True)
        # print "\n", "MergedDefaultOptions.__init__", "3333", "after update kwargs", options
        for name in self.__default_options__:
            setattr(self, name, options[name])
        if self.__default_options_check_unused__:
            unused_keys = list(set(kwargs.keys()) - set(self.__default_options__.keys()))
            if len(unused_keys) > 0:
                raise TypeError("invalid keyword arguments: " + str(unused_keys))
        if self.__default_options_pop_used__:
            for name in self.__default_options__:
                if name in kwargs: del kwargs[name]
        # print "\n", "MergedDefaultOptions.__init__", "4444", "after popping", kwargs
        # print "anyadbuzi!!!!", args, kwargs, self.__default_options_check_unused__, unused_keys
        super(MergedDefaultOptions,self).__init__(*args, **kwargs)



