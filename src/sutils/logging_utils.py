#!/usr/bin/env python
# project: sutils
# description: Smart Utilities
# file: sutils/logging_utils.py
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

from .primitives import qlist, qdict


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()


# -----------------------------------------------------------------------------
# LOG_FORMATS
# -----------------------------------------------------------------------------

LOG_FORMATS = qdict(
    short = "%(asctime)s\t%(levelname)s\t%(name)s:\t%(message)s",
    thread = "%(asctime)s\t%(levelname)s\t[tid:%(thread)x (%(threadName)s)]\t%(name)s:\t%(message)s",
    process = "%(asctime)s\t%(levelname)s\t[pid:%(process)d]\t%(name)s:\t%(message)s",
    full = "%(asctime)s\t%(levelname)s\t[pid:%(process)d tid:%(thread)x (%(threadName)s)]\t%(name)s:\t%(message)s",
)



# -----------------------------------------------------------------------------
# _add_logger
# -----------------------------------------------------------------------------

def _add_logger(obj, channel = None, root_channel = None, attr_name = "__logger" ):
    cls = obj
    channel = channel or cls.__name__
    root_channel = root_channel if root_channel is not None else cls.__module__
    if root_channel:
        channel = root_channel + '.' + channel
    if attr_name.startswith( '__' ): 
        attr_name = '_' + cls.__name__ + '__logger'
    setattr( obj, attr_name, logging.getLogger(channel) )



# -----------------------------------------------------------------------------
# @logged
# -----------------------------------------------------------------------------

@__all__.register
def logged(obj):
    _add_logger(obj, root_channel = '')
    return obj

