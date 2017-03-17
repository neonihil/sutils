#!/usr/bin/env python
# project: sutils
# description: Smart Utilities
# file: sutils/string_utils.py
# file-version: 0.1
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

import re
from .primitives import qlist

__all__ = qlist()

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
def underscorize(word):
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
