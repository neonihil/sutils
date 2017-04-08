# encoding: utf-8
# name: libfirebase
# version: @1.0
# author: Daniel Kovacs <dkovacs@firstpixel.com.au>
# file-name: gae.py
# file-description: Google App Engine helper classes
# file-version: 1.0
# @@{PACKAGE_LICENSE_HEADER}
#  
#

# -------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------

import os
import yaml
from .primitives import qdict, qlist


# -------------------------------------------------------------------------------
# exports
# -------------------------------------------------------------------------------

__all__ = qlist()


# -------------------------------------------------------------------------------
# cachedkeyproperty
# -------------------------------------------------------------------------------

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

