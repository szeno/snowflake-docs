# Nov 20, 2026: Failover group refreshes continue when a stream has an unsupported source object

When a database in a failover group contains a stream whose source object can’t be replicated, refreshing the secondary failover group
no longer fails. The refresh completes, and the stream is replicated as an unreadable stream in the secondary account. All other objects in the
failover group are replicated as usual.

This applies to streams on the following source objects:

- Tables or views in a database that isn’t in the same failover group as the stream.
- Tables or views in a database shared from another account.
- External tables.
- Event tables.

Previously, one such stream caused every refresh of the secondary failover group to fail, so the secondary account stopped receiving
updates until the stream was dropped or the database that contains its source object was added to the failover group.

Querying an unreadable stream in the secondary account returns an error that names the stream and the reason it can’t be read. If you
fail over to the secondary account, the stream remains unreadable there. After failback, the stream is also unreadable in the original
primary account and must be recreated.

For more information, see [Unreadable streams in a secondary account](/user-guide/account-replication-considerations#label-replication-streams-unreadable).
