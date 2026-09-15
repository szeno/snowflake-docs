# Apr 7, 2026: Workspaces replication (*General availability*)

Workspaces replication, which allows user workspaces to be included in database replication and failover operations, is now generally available.
When a workspace or its owning user is part of a replication or failover group, the workspace is copied to secondary accounts to support business
continuity and disaster recovery.

Replicated workspaces in secondary accounts are read-only. Files can be executed but not modified. When a secondary failover group is promoted
to primary, all contained workspaces become writable.

Note

Workspaces replication and failover require Business Critical Edition or higher.

For more information, see [Workspaces replication](/user-guide/ui-snowsight/workspaces-replication).
