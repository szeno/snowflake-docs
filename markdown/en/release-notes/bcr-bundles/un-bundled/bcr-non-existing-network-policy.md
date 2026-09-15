# CREATE USER command: NETWORK\_POLICY parameter must specify a valid network policy

Trying to add a network policy when creating a user behaves as follows:

Before the change:
:   When setting the `NETWORK_POLICY` parameter with the CREATE USER command, a user could:

    - Specify a non-existent network policy.
    - Execute the CREATE USER command using a role that did not have or inherit the OWNERSHIP privilege on the network policy.

After the change:
:   The following must be true to set the `NETWORK_POLICY` parameter when executing the CREATE USER command:

    - The network policy must exist.
    - The user executing the CREATE USER command must use a role that has or inherits the OWNERSHIP privilege on the specified network policy.

Ref: n/a
