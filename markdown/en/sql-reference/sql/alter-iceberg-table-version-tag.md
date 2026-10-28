# ALTER ICEBERG TABLE … VERSION\_TAG

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates, repoints, or drops a version tag on an [Apache Iceberg™ table](/user-guide/tables-iceberg). A version tag is a named
reference to a specific table snapshot that you can query with the [AT | BEFORE](/sql-reference/constructs/at-before) clause.

This command doesn’t set a [Snowflake governance tag](/user-guide/object-tagging/introduction).
To set a governance tag, use `ALTER ICEBERG TABLE ... SET TAG`.

See also:
:   [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table)

## Syntax

Copy code

```
ALTER ICEBERG TABLE [ IF EXISTS ] <table_name>
  CREATE [ OR REPLACE ] VERSION_TAG [ IF NOT EXISTS ] <tag_name>
    [ AS OF { VERSION <snapshot_id> | TIMESTAMP <timestamp_ms> } [ <retainClause> ] ]

ALTER ICEBERG TABLE [ IF EXISTS ] <table_name>
  ALTER VERSION_TAG <tag_name>
    AS OF { VERSION <snapshot_id> | TIMESTAMP <timestamp_ms> }

ALTER ICEBERG TABLE [ IF EXISTS ] <table_name>
  REPLACE VERSION_TAG <tag_name>
    AS OF { VERSION <snapshot_id> | TIMESTAMP <timestamp_ms> } [ <retainClause> ]

ALTER ICEBERG TABLE [ IF EXISTS ] <table_name>
  DROP VERSION_TAG [ IF EXISTS ] <tag_name>
```

Where:

> Copy code
>
> ```
> retainClause ::=
>   RETAIN <num> { DAYS | HOURS | MINUTES }
> ```

## Parameters

`table_name`
:   Identifier for the table to modify.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CREATE [ OR REPLACE ] VERSION_TAG [ IF NOT EXISTS ] tag_name`
:   Creates a version tag named `tag_name` on the table.

    Tag names are case-sensitive and are stored as you write them. A tag name must be non-empty, can’t be `main` in any letter case,
    and can’t match the name of an existing branch on the same table. Enclose a name that isn’t a valid unquoted identifier in double
    quotes.

    Without `OR REPLACE` or `IF NOT EXISTS`, the command fails if a tag with the same name already exists.

    `OR REPLACE` repoints an existing tag to the specified snapshot, or creates the tag if it doesn’t exist.

    `IF NOT EXISTS` leaves an existing tag unchanged, including its retention period.

    You can’t specify both `OR REPLACE` and `IF NOT EXISTS` in the same statement.

`ALTER VERSION_TAG tag_name`
:   Repoints an existing version tag to a different snapshot. The tag must already exist; otherwise, the command fails.

    The `AS OF` clause is required. To change the retention period of a tag, use `REPLACE VERSION_TAG` instead.

`REPLACE VERSION_TAG tag_name`
:   Repoints an existing version tag to a different snapshot and, optionally, sets a new retention period. The tag must
    already exist; otherwise, the command fails.

    The `AS OF` clause is required.

`DROP VERSION_TAG [ IF EXISTS ] tag_name`
:   Removes a version tag from the table. Queries that specify the tag fail after the tag is dropped.

    `IF EXISTS` makes the command succeed when the tag doesn’t exist.

    Dropping a tag doesn’t delete data files. It doesn’t affect other tags, even when they reference the same snapshot.

`AS OF VERSION snapshot_id`
:   Identifies the snapshot to tag by its Iceberg snapshot ID, which is a positive integer. To list the snapshot IDs available for a
    table, see [Find a snapshot to tag](/user-guide/tables-iceberg-time-travel#label-tables-iceberg-time-travel-find-snapshot).

`AS OF TIMESTAMP timestamp_ms`
:   Identifies the snapshot to tag by time, expressed as an integer number of milliseconds since the Unix epoch. Snowflake tags
    the most recent snapshot committed at or before that time. If no snapshot was committed at or before that time, the command fails.

`RETAIN num { DAYS | HOURS | MINUTES }`
:   Sets how long the tag is kept, measured from the time the tagged snapshot was committed. `num` must be a positive integer.

    Snowflake stores this value as the `max-reference-age-ms` property of the reference in the Iceberg table metadata, so other query
    engines observe the same retention period.

    If you omit this clause when you create a tag, the tag has no age-based expiration and is kept until you drop it.
    If you omit this clause when you repoint an existing tag, the tag keeps its current retention period.

    Default: no age-based expiration

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Iceberg table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | External volume |  |
| USAGE | Catalog integration | Required if the table uses a catalog integration. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Only the table owner (that is, the role with the OWNERSHIP privilege on the table) or higher can execute this command. Querying
  a table at a version tag requires the USAGE privilege on the database and schema and the SELECT privilege on the table.
- If you omit the `AS OF` clause when you create a tag, the tag references the table’s current snapshot. If the table has no
  current snapshot, the command fails.
- The `RETAIN` clause is valid only with `AS OF` on `CREATE VERSION_TAG` and `REPLACE VERSION_TAG`. You can’t specify `RETAIN`
  without `AS OF`, and `ALTER VERSION_TAG` doesn’t accept `RETAIN`.
- Iceberg stores tags and branches in a single namespace, so a tag and a branch on the same table can’t share a name.
- On an externally managed table that uses an Iceberg REST catalog, the command commits the change to that catalog. On other
  catalog types, Snowflake records the tag in the Iceberg metadata it has already refreshed. Refresh the table before you query a
  tag that another engine created. If the table uses automated refresh, the next refresh picks up the tag. See
  [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh). If another engine commits to the table at the same time, the command can fail
  with a conflict. When it fails, the tag isn’t created or modified, and you can retry the command.
- On a Snowflake-managed table, the tag is available to queries in Snowflake immediately, and appears in the Iceberg table metadata
  after Snowflake next updates that metadata.
- On a Snowflake-managed table, while a version tag references a snapshot, Snowflake retains that snapshot and the data files
  it needs, even if the table’s
  [data retention period](/user-guide/tables-iceberg-metadata#label-tables-iceberg-time-travel-retention-period) has elapsed.

For more information, see [Time Travel for Apache Iceberg™ tables](/user-guide/tables-iceberg-time-travel).

## Examples

Create a version tag that references the table’s current snapshot:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table CREATE VERSION_TAG end_of_quarter;
```

Create a version tag that references a specific snapshot, and keep it for seven days after that snapshot was committed:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CREATE VERSION_TAG audit_2026_q1 AS OF VERSION 3821550127947089009 RETAIN 7 DAYS;
```

Create a version tag that references the most recent snapshot committed at or before a point in time:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CREATE VERSION_TAG before_backfill AS OF TIMESTAMP 1764547200000;
```

Create a version tag only if it doesn’t already exist:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CREATE VERSION_TAG IF NOT EXISTS nightly AS OF VERSION 3821550127947089009;
```

Repoint an existing version tag to a different snapshot:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  ALTER VERSION_TAG nightly AS OF VERSION 7245108833619203344;
```

Create the tag if it doesn’t exist, or repoint it if it does, and set a retention period:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CREATE OR REPLACE VERSION_TAG nightly AS OF VERSION 7245108833619203344 RETAIN 48 HOURS;
```

Repoint an existing version tag and set a new retention period:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  REPLACE VERSION_TAG nightly AS OF VERSION 7245108833619203344 RETAIN 48 HOURS;
```

Query the table at a version tag:

Copy code

```
SELECT * FROM my_iceberg_table AT(VERSION_TAG => 'audit_2026_q1');
```

Drop a version tag:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table DROP VERSION_TAG IF EXISTS nightly;
```
