#!/usr/bin/env python
# project: ulws
# description: Ultra Light Web Server
# file: ulws/__init__.py
# file-version: 1.0
# author: DANA <dana@deasys.net>
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

__author__ = "DANA"
__email__ = "dana@deasys.net"
__description__ = "Smart Utilities"
__license__ = "GPLv3+"
__uri__ = "https://github.com/ultralightweight/sutils"
__version__ = "0.3.0"

from .primitives import *
from .logging_utils import *
from .string_utils import *
from .meta_patterns import *
import _json as json
