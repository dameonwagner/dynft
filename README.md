# dynft

Dynamic ruleset object management for nftables.

## DESCRIPTION

`dynft` is inspired by `ipset` functionality that was added to an in-house
tool used at the University of Oxford's IT Services Department's Unix Platform
Services Team, called "`netoptions`", designed for the purpose of managing and
updating IP address sets (IPv6 and IPv4) declared using only FQDNs in a
configuration file, with addresses resolved at runtime.

Having migrated from separately managed `ipset` "sets" and `iptables` "rules",
to `nftables` where sets and rules are all defined within the same context, a
new tool was needed.

The approach is similar, in that a YAML format configuration file
"`/etc/nftables_dynamic.yml`" describes any `sets` that you would like to be
regularly "refreshed" based on DNS resolution.

While the tool can be run manually, systemd "service" and "timer" unit files
are provided that will trigger the desired sets to be refreshed every 15
minutes (if a different periodicity is needed, the systemd "timer" can be
overridden with a drop-in file (see systemd.unit(5) for details).

----

<!-- Copyright (C) 2024  Dameon Wagner -->
