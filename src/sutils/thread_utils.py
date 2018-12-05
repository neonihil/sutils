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


# -----------------------------------------------------------------------------
# imports
# -----------------------------------------------------------------------------

from threading import Thread
from queue import Queue, Empty


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

from .primitivies import qlist
__all__ = qlist()


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

