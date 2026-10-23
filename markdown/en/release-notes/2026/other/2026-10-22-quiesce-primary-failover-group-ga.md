# Oct 22, 2026: Quiesce a primary failover group (*General availability*)

Read-only mode for primary failover groups is now generally available.

You can put a primary failover group into read-only mode for a planned disaster recovery drill or
account migration. Read-only mode stops new writes to objects in the failover group on the source
account, so no data changes occur on the primary while you run a final replication refresh and fail
over.

For more information, see [Quiesce a primary failover group](/user-guide/account-replication-quiesce-primary).
