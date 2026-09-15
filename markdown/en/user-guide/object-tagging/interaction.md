# How tags interact with Snowflake features

## Replication

Tags and their assignments can be replicated from a source account to a target account.

Tag assignments cannot be modified in the target account after the initial replication from the source account. For example,
setting a tag on a secondary (i.e. replicated) database is not allowed. To modify tag assignments in the target account, modify
them in the source account and replicate them to the target account.

For [database replication](/user-guide/database-replication-considerations), the replication operation fails if either of the
following conditions is true:

- The primary database is in an Enterprise (or higher) account and contains a tag but one or more of the accounts approved for
  replication are on lower editions.
- An object contained in the primary database has a [dangling reference](/user-guide/database-replication-considerations#label-database-replication-dangling-references) to a tag in
  a different database.

To avoid a dangling reference error, replicate the database and account-level objects
using a [replication or failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups). Ensure that the replication group includes:

- The database containing the tags in the `ALLOWED_DATABASES` property.
- Other account-level objects that have a tag in the `OBJECT_TYPES` property (e.g. `ROLES`, `WAREHOUSES`).

  For details, refer to [CREATE REPLICATION GROUP](/sql-reference/sql/create-replication-group) and [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group).

Note

When using replication and failover groups or database replication:

- Failover/failback features are only available to Snowflake accounts that are Business Critical Edition (or higher).

  For more information, refer to [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).
- If you specify the `IGNORE EDITION CHECK` clause for database replication in an
  [ALTER DATABASE](/sql-reference/sql/alter-database) statement or in a CREATE OR ALTER statement
  for a replication or failover group, tag replication can occur when the target account is a lower edition than
  [Business Critical](/user-guide/intro-editions).

  For details, refer to the clause description in these commands.

## Cloning

- Tag associations in the source object (e.g. table) are maintained in the cloned objects.
- For a database or a schema:

  When a database or schema is cloned, tags that reside in that schema or database are also cloned.

  If a table or view exists in the source schema/database and has references to tags in the same schema or database, the cloned table or view is mapped to the corresponding cloned tag (in the target schema/database) instead of the tag in the source schema or database.

## Data sharing

- When the shared view and tag exist in different databases, grant the REFERENCE\_USAGE privilege on the database containing the tag to the
  share. For information, see [Share data from multiple databases](/user-guide/data-sharing-multiple-db).
- In the data sharing consumer account:
  - Executing the [SHOW TAGS](/sql-reference/sql/show-tags) command returns the shared tag, provided that the role executing the SHOW TAGS command
    has the USAGE privilege on the schema containing the shared tag.

    If the provider grants the READ privilege on the tag to the share or to a shared database role, the consumer can view the tag
    assignments for the shared tag. For information, see [shared tag references](/user-guide/data-sharing-provider#label-share-tag-references).
  - If a tag from the data sharing provider account is assigned to a shared table, the data sharing consumer cannot call the
    [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) function or the [TAG\_REFERENCES](/sql-reference/functions/tag_references) Information Schema table
    function to view the tag assignment.
