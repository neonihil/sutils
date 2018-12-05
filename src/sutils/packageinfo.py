#!/usr/bin/env python
# project: sutils
# description: Smart Utilities
# file: sutils/packageinfo.py
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

import os
import yaml
from .primitives import qdict, qlist


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------

__all__ = qlist()


# -----------------------------------------------------------------------------
# PackageInfo
# -----------------------------------------------------------------------------

@__all__.register
class PackageInfo(qdict):

    def __init__(self, package_home, name = None, description = None, version = None, package_info_path = None, debug = True ):
        self.package_home = package_home
        self.name = name
        self.description = description
        self.version = version
        self.debug = debug
        self.package_info_path = package_info_path or os.path.join(self.package_home, 'package.yaml')
        if (os.path.isfile(self.package_info_path)):
            self.load_package_info()

    def load_package_info(self, path = None):
        path = path or self.package_info_path
        info = yaml.load(open(path, 'r').read())
        tier = info.get('tier', 'dev')
        tier_info = info.pop("tiers", None)
        self.update(info, recursive = True, add_keys = True, convert_to_qdict = True)
        if tier_info and tier_info.get(tier,None):
            self.update(tier_info[tier], recursive = True, add_keys = True, convert_to_qdict = True)

