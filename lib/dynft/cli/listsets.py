# `dynft listsets`: Check the config for the existence of sets, and if they
# exist, print a YAML representation to stdout.
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

import sys
import click
import yaml

config = None

@click.command(
    help='Print any configured dynamically managed sets, and exit')
@click.pass_context
def listsets(__ctx):
    """`listsets` is only marginally more complicated than `hassets`.  The only
    difference is to print the defined sets in YAML format.
    """
    global config
    config = __ctx.obj['CONFIG']

    if not config.sets or not isinstance(config.sets, dict):
        sys.exit(2)
    else:
        print(yaml.dump(config.sets, indent=2).strip())
        sys.exit(0)

if __name__ == '__main__':
    print('Cannot run independently, please use `dynft listsets` instead')
    sys.exit(1)
