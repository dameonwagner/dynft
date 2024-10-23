=====
dynft
=====

-----------------------------------------------
Dynamic ruleset object  management for nftables
-----------------------------------------------

:Date: 2024-08-21
:Version: 0.0.1
:Manual section: 8
:Manual group: nftables dynamic management

.. :Author: dameon.wagner@it.ox.ac.uk
.. :Copyright: 2024 Dameon Wagner
.. :Licence: GPL-3

Synopsis
--------

dynft [OPTIONS] COMMAND [COMMAND_ARGS [...] ]

Description
-----------

``dynft`` is a command-line tool used to dynamically update some ruleset
objects used by nftables.  Currently only ``set`` objects are supported.

Global Options
--------------

`-V`, `--verbose`

    Provide verbose, or additional, output, such as the JSON command data that
    will be applied to the nftables ruleset.

`--help`

    Show usage message.

Commands
--------

The following subcommands are supported.  Each of which support a `--help`
option of their own.

``hassets``

    Exits with a return code of 0 if sets have been defined in the
    configuration file, otherwise exits with a return code of 2.

``listsets``

    Lists the sets defined in the configuration file, if defined, otherwise
    exits with a return code of 2.

``refreshsets [OPTIONS]``

    Walks the sets defined in the configuration file, and refreshes the
    active membership of each based upon the configuration (this will both add
    and remove members, as necessary, in a single atomic action).

    The following options can be used with this subcommand:

    `-d`, `--dry-run`

        Do not actually update the ruleset, just show what would be applied.

    `-V`, `--verbose`
    
        Provide verbose output (this is equivalent to the global option of the
        same name).

Configuration File
------------------

``dynft`` requires a simple `YAML` formatted configuration file named
``/etc/nftables_dynamic.yml``.  The data structure is relatively simple, with
currently only a single top-level dictionary called ``sets``.  For each `set`
that you wish to regularly update the member element list of provided as a
named key within the dictionary.

Each `set` is itself a dictionary data structure that has a single required
variable: `members`.  `members` should be a list containing items for each
desired element member (or members), and can be of two forms:  `host` or
`literal`.

``host``

    Member items should contain a valid DNS FQDN (Fully Qualified Domain Name)
    that will be resolved in the DNS at runtime and the resulting IP address
    (or addresses, if the name in the DNS resolves to a round-robin collection
    of addresses) will be included as an element in the set to be applied to
    the nftables ruleset.  DNS CNAME records will be followed to any eventual
    ``A`` or ``AAAA`` records.  The FQDN will additionally be used as the
    `comment` in the applied set, for easy cross reference.

    If the DNS query returns an ``NXDOMAIN`` response (i.e. there is no
    matching ``A`` or ``AAAA`` record in DNS), the listed member will be
    silently excluded from the applied set.  If the result of running ``dynft``
    does not include the elements you expect, please use DNS querying tools
    such as ``host`` or ``dig`` to troubleshoot.

``literal``

    Member items should contain either a valid IPv6 or IPv4 address.  A reverse
    DNS query will be attempted to discover a usable FQDN from any ``PTR``
    record returned.  If no ``PTR`` record is found (i.e. the DNS query
    returned ``NXDOMAIN``), the element's comment will be "IP-LITERAL",
    otherwise the value of the record is used as the element's comment, which
    should have been returned from the DNS as a valid FQDN.

Optional Set variables
~~~~~~~~~~~~~~~~~~~~~~

`sets` defined in the configuration file can optionally also define other
variables, for cases where you want to be explicit, otherwise sane defaults
will be used.

``family``

    A `set` needs to be contained within a table, which itself requires being
    declared with an ``Address Family``.  ``nftables`` supports various address
    families, but for ``dynft`` the supported families are: ``inet`` (a hybrid
    family which supports both IPv6 and IPv4 packet processing), ``ip6`` (which
    supports only IPv6), and ``ip`` (which supports only IPv4).  In the vast
    majority of cases the default of ``inet`` will be acceptable.

``table``

    Tables are containers for ``chains``, ``sets``, and other stateful objects
    within a ``nftables`` ruleset.  They are identified by their Address
    ``family`` (see above), and their name.  If no ``table`` variable is
    provided within a `set` definition, the default value of ``filter`` will be
    used.

``type``

    `sets` can contain various types of elements, but currently for ``dynft``
    the supported types are: ``ipv6_addr`` (which supports IPv6 addresses as
    elements), and ``ipv4_addr`` (which supports IPv4 addresses as elements).
    If a set configuration does not declare a ``type`` variable, **two** sets
    will be created/managed, one for IPv6 addresses (where the set's name is
    suffixed with "_v6", and a ``type`` of ``ipv6_addr``), and one for IPv4
    addresses (where the set's name is suffixed with "_v4", and a ``type`` or
    ``ipv4_addr``).

If either ``family`` or ``type`` are explicitly defined, rather than relying on
the defaults, they need to be compatible (so you can't have an ``ip`` family
with ``ipv6_addr`` sets, and vice versa).  Additionally, the ``family``
variable, if defined, needs to match the ``family`` the ``table`` was defined
with.

If your active nftables ruleset is mostly contained within an `inet` family
table named `filter`, these optional variables can be ignored.

Example configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple configuration example, for a system that needs to fetch SAML metadata,
may look like the following::

 ---
 sets:
   shibboleth_metadata_sources:
     members:
       - host: metadata.ukfederation.org.uk
       - host: mdq.ukfederation.org.uk
       - literal: 2603:1020:702:3::12
       - literal: 4.159.3.235
 ...

The above, would create/update two `sets` in the nftables ruleset, named:

*   shibboleth_metadata_sources_v6
*   shibboleth_metadata_sources_v4

Each of which would contain elements of their respective address address
family, with details returned from DNS as available or appropriate.

Files
-----

`/etc/nftables_dynamic.yml`

    Global system configuration, as described in the
    `Configuration File`_ section.

Exit Values
-----------

``0``   Success

``2``   No sets defined in the configuration file

``32``  IPSet has no supplied name

``33``  IPSet is configured with an invalid ``family``

``34``  IPSet is configured with an invalid ``type``

``35``  IPSet is configured with a ``family`` and ``type`` mismatch

``255`` Invalid configuration file contents

See Also
--------

``nft(8)``, ``libnftables-json(5)``, ``dig(1)``, ``host(1)``
