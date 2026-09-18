# ALTER ICEBERG TABLE … ADD | DROP | REPLACE PARTITION BY

Adds, drops, or replaces partition fields for a Snowflake-managed [Apache Iceberg™ table](/user-guide/tables-iceberg).

See also:
:   [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table)

## Syntax

Copy code

```
ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> ADD PARTITION BY ( <partitionExpression> )

ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> DROP PARTITION BY ( <partitionExpression> )

ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> REPLACE PARTITION BY ( <oldPartitionExpression> ) WITH ( <newPartitionExpression> )
```

For `partitionExpression`, `oldPartitionExpression`, and `newPartitionExpression` syntax, see [Partition expression parameters](#partition-expression-parameters-partitionexpression).

## Parameters

`table_name`
:   Identifier for the table to modify.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ADD PARTITION BY ( partitionExpression )`
:   Adds a partition field to the table’s current partition spec.
    New data written after the command completes uses the updated partition spec.

    Existing data isn’t rewritten when you add a partition field.

`DROP PARTITION BY ( partitionExpression )`
:   Removes a partition field from the table’s current partition spec.
    New data written after the command completes uses the updated partition spec.

    Existing data isn’t rewritten when you drop a partition field.

`REPLACE PARTITION BY ( oldPartitionExpression ) WITH ( newPartitionExpression )`
:   Replaces a partition field in the table’s current partition spec with a new partition field.
    New data written after the command completes uses the updated partition spec.

    Existing data isn’t rewritten when you replace a partition field.

## Partition expression parameters (`partitionExpression`)

Copy code

```
partitionExpression ::=
  <col_name>                            -- identity transform
  | BUCKET ( <num_buckets> , <col_name> )
  | TRUNCATE ( <width> , <col_name> )
  | YEAR ( <col_name> )
  | MONTH ( <col_name> )
  | DAY ( <col_name> )
  | HOUR ( <col_name> )
```

`oldPartitionExpression` and `newPartitionExpression` use the same syntax. In a REPLACE PARTITION BY command,
`oldPartitionExpression` must match a partition field in the table’s current partition spec.

Snowflake supports all partition transforms in version 2 of the Apache Iceberg specification. For more information, see
[Partition Transforms](https://iceberg.apache.org/spec/#partition-transforms) in the Apache Iceberg specification.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Iceberg table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Only the table owner (that is, the role with the OWNERSHIP privilege on the table) or higher can execute this command.
- Partition evolution is only supported for tables that use Snowflake as the Iceberg catalog (Snowflake-managed Iceberg tables).
- Exactly one partition field can be changed per command. Multiple partition expressions aren’t supported.
- After adding, dropping, or replacing a partition field, if the new partition spec is compatible with an existing partition spec defined on the table, Snowflake reuses the existing partition spec.
- Dropping a column that is part of the current or any historical partition spec defined on the table isn’t supported.
- You can’t enable clustering on a table that is currently partitioned or has ever had partition transforms defined on it. This restriction applies even if all partition fields have been dropped and the table is no longer partitioned.

## Examples

The following example adds a partition field that distributes data into 10 buckets based on the value of `col1`:

Copy code

```
ALTER ICEBERG TABLE myTable ADD PARTITION BY (BUCKET(10, col1));
```

The following example drops the identity partition field based on `col2`:

Copy code

```
ALTER ICEBERG TABLE myTable DROP PARTITION BY (col2);
```

The following example replaces the partition field that distributes data into 10 buckets based on `col1` with a
partition field that distributes data into 20 buckets:

Copy code

```
ALTER ICEBERG TABLE myTable REPLACE PARTITION BY (BUCKET(10, col1)) WITH (BUCKET(20, col1));
```

To view all partition specs defined on the table and the ID of the partition spec currently in use:

Copy code

```
SHOW ICEBERG TABLES LIKE 'myTable'
  ->> SELECT "partition_specs", "current_partition_spec_id" FROM $1;
```
