# Dec 10, 2025: General availability of WORM backups

WORM (Write Once, Read Many) backups are now generally available to all accounts.

Backups help organizations protect critical data against modification or deletion. Backups represent discrete
point-in-time copies of Snowflake objects. You choose which objects to back up (tables, schemas, or databases),
how frequently to back them up, how long to keep the backups, and whether to add a retention lock so that they
can’t be deleted prematurely.

Key use cases for backups include:

- **Regulatory compliance**: Backups with retention lock help organizations, financial institutions, and related
  industries address regulations that require records to be retained in an immutable format.
- **Recovery**: Backups help organizations create discrete copies to protect and recover business-critical data
  in case of accidental modifications or deletions.
- **Cyber resilience**: Backups with retention lock are part of an overall cyber-resilience strategy. They help
  organizations protect business-critical data during cyber attacks, especially ransomware attacks. The retention
  lock ensures that this data can’t be deleted by the attacker, even if they gain access to the account by using
  the ACCOUNTADMIN or ORGADMIN roles.

For more information, see [Backups for disaster recovery and immutable storage](/user-guide/backups).

## Terminology change

The feature is now called **backups** instead of snapshots. All SQL commands, views, and privileges use
**BACKUP** terminology:

- CREATE BACKUP POLICY, CREATE BACKUP SET
- ALTER BACKUP POLICY, ALTER BACKUP SET
- DROP BACKUP POLICY, DROP BACKUP SET
- SHOW BACKUP POLICIES, SHOW BACKUP SETS, SHOW BACKUPS IN BACKUP SET
- BACKUPS, BACKUP\_POLICIES, BACKUP\_SETS views in Account Usage, Organization Usage, and Information Schema
- APPLY BACKUP RETENTION LOCK privilege

The former SNAPSHOT/SNAPSHOTS names are still present but deprecated in favor of their BACKUP/BACKUPS equivalents.
For example:

- CREATE SNAPSHOT POLICY is deprecated; use CREATE BACKUP POLICY instead.
- SNAPSHOTS view is deprecated; use BACKUPS view instead.
- APPLY SNAPSHOT RETENTION LOCK privilege is deprecated; use APPLY BACKUP RETENTION LOCK privilege instead.

The deprecated commands, views, and privileges continue to work, but Snowflake intends to remove them in a future release.
