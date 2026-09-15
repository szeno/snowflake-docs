# May 8, 2026: Tuple format support for ingress private endpoint identifiers in network rules

You can now specify tuple values for ingress private endpoint identifiers in network rules.
This feature allows PrivateLink identifiers such as `AWSVPCEID`, `AZURELINKID`, and
`GCPPSCID` to use tuple syntax that combines endpoint identifiers with IP addresses
and/or CIDR ranges.

This new tuple syntax applies to network rules used for ingress mode.

For more information, see [Network rules](/user-guide/network-rules), [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule),
and [ALTER NETWORK RULE](/sql-reference/sql/alter-network-rule).
