# Aug 18, 2025: Write Once, Read Many (WORM) snapshots (*Preview*)

The Write Once, Read Many (WORM) snapshots feature is now in [Preview](/release-notes/preview-features).

WORM snapshots represent backups of specific Snowflake tables, schemas, or databases.
These backups are *immutable*: they can’t be changed after being created.
Snowflake manages all the snapshots of a specific object within a single container object, the snapshot set.
You can establish snapshot policies that determine how often to automatically take new snapshots, when to automatically
delete old snapshots, and when to prevent important snapshots from being deleted, even by privileged users.

For more information, see: [Backups for disaster recovery and immutable storage](/user-guide/backups).
