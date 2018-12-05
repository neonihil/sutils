#!/usr/bin/env python
# project: sutils
# description: Smart Utilities
# file: sutils/annotations.py
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


from .primitives import qdict


# -----------------------------------------------------------------------------
# Annotation
# -----------------------------------------------------------------------------

class Annotation(object):

    def __init__(self, base_field):
        self.base_field = base_field


    def set(self, obj, path, value ):
        if not isinstance(path, list):
            path = list(path)
        path.append(self.base_field)
        node = obj
        print "\n\n set", "-"*50, obj, path, value
        while path:
            key = path.pop()
            print "---->", key, node
            if len(path) == 0:
                setattr(node,key,value)
                return node
            if not hasattr(node,key):
                setattr(node,key,qdict())
            node = getattr(node,key)


    def get(self, obj, path, default = None):
        if not isinstance(path, list):
            path = list(path)
        path.append(self.base_field)
        node = obj
        print "\n\n get", "-"*50, obj, path, default
        while path:
            key = path.pop()
            print "---->", key, node
            if not hasattr(node,key):
                if len(path) == 0:
                    setattr(node,key,default)
                else:
                    setattr(node,key,qdict())
            node = getattr(node,key)
        return node


    def append(self, obj, path, value):
        annotation = self.get(obj, path, [] )
        annotation.append(value)
        return annotation


