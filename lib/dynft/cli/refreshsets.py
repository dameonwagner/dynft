# `dynft refreshsets`: Parse any sets defined in the config, and build a JSON
# data structure compliant with that described in libnftables-json(5), and if
# running as root (and not in dry-run mode) apply the changes to the nftables
# ruleset.
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
import click
import json
import pprint
import nftables

from dynft import IPSet, IPSetException

pp = pprint.PrettyPrinter().pprint

nft = nftables.Nftables()
nft.set_json_output(True)

config = None

@click.command(
    help='Flush and update configured dynamically managed sets.')
@click.option(
    '--dry-run', '-d', is_flag=True, default=False,
    help='Do not actually update the ruleset, just show what would be applied'
)
@click.option(
    '--verbose', '-V', is_flag=True, default=False,
    help='Provide verbose output'
)
@click.pass_context
def refreshsets(__ctx, dry_run, verbose):
    """Build a full JSON blob acceptible for executing with libnftables'
    `json_cmd` function, and apply the update to the running nftables ruleset
    (or just display on stdout if in "verbose" mode, and either in "dry-run"
    mode, or running as a user other than root.
    """
    global config
    config = __ctx.obj['CONFIG']

    # Interaction with nftables requires root access, so enforce `dry_run` if
    # not running as root
    dry_run = True if os.getuid() != 0 else dry_run

    if not config.verbose and verbose:
        config.verbose = True

    if not config.sets or not isinstance(config.sets, dict):
        sys.exit(2)

    live_sets = [
        set.get('set') for set in json.loads(
            nft.cmd('list sets')[1]).get('nftables') if set.get('set')
    ] if not dry_run else []

    # While sets are defined in the configuration, we will always create both
    # an IPv6 and an IPv4 variant, using the name supplied in the
    # configuration, but suffixed with "_v6" or "_v4" as appropriate.
    managed_sets = []
    for managed_set in config.sets:
        this_set = config.sets[managed_set]
        if not this_set.get('type') and not this_set.get('family'):
            this_setv6 = IPSet(this_set, name=managed_set+'_v6', type='ipv6_addr')
            managed_sets.append(this_setv6)
            this_setv4 = IPSet(this_set, name=managed_set+'_v4', type='ipv4_addr')
            managed_sets.append(this_setv4)
        else:
            try:
                managed_sets.append(IPSet(this_set, name=managed_set))
            except IPSetException as IPSE:
                # The configured set defintions could be invalid.  Known issues
                # could be caught and handled appropriately.
                #
                # If a set's family and type clash, ignore the set and carry
                # on silently (or throw a warning to stderr if running in
                # verbose mode.
                if IPSE.errno == IPSE.FAMILY_TYPE_MISMATCH:
                    if config.verbose:
                        print('WARNING: Set "{}": {}'.format(
                            managed_set, IPSE.msg), file=sys.stderr)
                    continue
                # Otherwise bubble the exception up further.
                else:
                    raise IPSE

    # Build the complete JSON command blob.  Applying all the desired changes
    # in a single nftables `json_cmd()` invocation is as close to an atomic
    # change as is possible.  If the set already exists in the live ruleset, we
    # want to flush it first.
    refresh_cmd = dict(nftables=[])
    for managed_set in managed_sets:
        if managed_set.name in [ set.get('name') for set in live_sets ]:
            refresh_cmd['nftables'].append(managed_set.flush_cmd())
        refresh_cmd['nftables'].append(managed_set.add_cmd())

    # If running in dry-run mode (implicit when running as a non root user),
    # and verbose output was requested, pretty print the object representation
    # of what would be applied to nftables' json_cmd (it's not proper JSON, as
    # it uses single rather than double quotes, but that's just the way
    # python-nftables works...
    if (os.getenv('DEBUG') or config.verbose) and dry_run:
        pp(refresh_cmd)

    if nft.json_validate(refresh_cmd):
        # `nft.json_validate` does indeed only validate the passed JSON-like
        # object.  Try to catch and handle any exceptions, as it's still
        # possible to include unsupported data that will make libnftables barf.
        try:
            if not dry_run: nft.json_cmd(refresh_cmd)
        except e as JCE:
            print(JCE, file=sys.stderr)
    else:
        print('Proposed command is not valid', file=sys.stderr)
        sys.exit(255)
# refreshsets()


if __name__ == '__main__':
    print('Cannot run independently, please use `dynft refreshsets` instead')
    sys.exit(1)
