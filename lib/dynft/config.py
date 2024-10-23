# Config class for dynft.  Load the serialised config for global use dynft
# 
# Copyright (C) 2024  Dameon Wagner
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

import os
import sys
import yaml

##############################################################################
# Module constants
#

DEFAULT_CONFIG_FILE = '/etc/nftables_dynamic.yml'

##############################################################################
# Defined classes
#

class Config:
    """
    A class used to represent the contents of `dynft`'s configuration, which
    should be found serialized in YAML format in "/etc/nftables_dynamic.yml".

    Currently "sets" are the only nftables object supported for dynamic
    management.

    Example YAML structure:

    #---8<-----------------------------------------------------------------
    ---
    sets:
      shibboleth_metadata_sources:
        members:
          - host: metadata.ukfederation.org.uk
          - host: mdq.ukfederation.org.uk
          - literal: 2603:1020:702:3::12
          - literal: 4.159.3.235
    ...
    #---8<-----------------------------------------------------------------
    """

    def __init__(self):
        try:
            self.__dict__.update(
                yaml.safe_load(open(DEFAULT_CONFIG_FILE, 'r'))
            )
        except FileNotFoundError as FNFE:
            raise ConfigException(str(FNFE), ConfigException.CONFIG_ERROR)
        except yaml.parser.ParserError as y:
            raise ConfigException(str(y), ConfigException.CONFIG_ERROR)
        except TypeError as TE:
            if "'NoneType' object is not iterable" in TE.args:
                print('Active config is imvalid or empty', file=sys.stderr)
                sys.exit(255)
            else:
                raise TE
    # __init__()

    def load(self, config=None):
        """Load additional/replacement configuration, not yet implemented."""
        pass
    # load()

    def dump(self):
        """Return internal representation of the current config."""
        return self.__dict__
    # dump()
# class:Config


##############################################################################
# Exception classes
#

class ConfigException(Exception):
    CONFIG_ERROR = 254
    def __init__(self, msg, errno=255):
        self.msg = msg
        self.errno = errno
