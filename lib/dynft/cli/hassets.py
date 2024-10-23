# `dynft hassets`: Simply check the config for the existence of sets, and
# return 0 if there are any.  A non-zero return code should inform the caller
# that there's no point in trying to refresh any sets.
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

config = None

@click.command(
    help='Determine if any dynamically managed sets are configured, and exit')
@click.pass_context
def hassets(__ctx):
    """For `hassets`, all we want to do is return an exit code of 0 (true) if
    we do have sets defined in the config, or non-zero if we don't.
    """
    global config
    config = __ctx.obj['CONFIG']

    if not config.sets or not isinstance(config.sets, dict):
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == '__main__':
    print('Cannot run independently, please use `dynft hassets` instead')
    sys.exit(1)
