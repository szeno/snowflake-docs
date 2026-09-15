# DROP SCHEMA

Removes a schema from the current/specified database.

See also:
:   [CREATE SCHEMA](/sql-reference/sql/create-schema) , [ALTER SCHEMA](/sql-reference/sql/alter-schema) , [DESCRIBE SCHEMA](/sql-reference/sql/desc-schema) , [SHOW SCHEMAS](/sql-reference/sql/show-schemas) , [UNDROP SCHEMA](/sql-reference/sql/undrop-schema)

## Syntax

Copy code

```
DROP SCHEMA [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Parameters

`name`
:   Specifies the identifier for the schema to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    If the schema identifier is not fully-qualified (in the form of `db_name.schema_name`), the command looks for the schema
    in the current database for the session.

`CASCADE | RESTRICT`
:   Specifies whether the schema can be dropped if foreign keys exist that reference any tables in the schema:

    - `CASCADE` drops the schema and all objects in the schema, including tables with primary/unique keys that are referenced by
      foreign keys in other tables.
    - `RESTRICT` returns a warning about existing foreign key references and does not drop the schema.

    Default: `CASCADE`

## Usage notes

- Dropping a schema does not permanently remove it from the system. A version of the dropped schema is retained in
  [Time Travel](/user-guide/data-time-travel) for the number of days specified by the `DATA_RETENTION_TIME_IN_DAYS`
  parameter for the schema:

  1. Within the Time Travel retention period, a dropped schema can be restored using the [UNDROP SCHEMA](/sql-reference/sql/undrop-schema) command.
  2. When the Time Travel retention period ends, the next state for the dropped schema depends on whether it is permanent or transient:

     - A permanent schema moves into [Fail-safe](/user-guide/data-failsafe). In Fail-safe (7 days), a dropped schema can be
       recovered, but only by Snowflake. When the schema leaves Fail-safe, it is purged.
     - A transient schema has no Fail-safe, so it is purged when it moves out of Time Travel.
  3. Once a dropped schema has been purged, it cannot be recovered; it must be recreated.
- Currently, when a schema is dropped, the data retention period for child tables, if explicitly set to be different from the retention
  of the schema, is not honored. The child tables are retained for the same period of time as the schema. To honor the data retention
  period for these tables, drop them explicitly before you drop the schema.
- After dropping a schema, creating a schema with the same name creates a new version of the schema. The dropped version of the previous
  schema can still be restored using the following method:

  1. Rename the current version of the schema to a different name.
  2. Use the [UNDROP SCHEMA](/sql-reference/sql/undrop-schema) command to restore the previous version.
- In a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) that allows writes, this command
  simultaneously drops the schema from your catalog-linked database and its corresponding namespace from your remote catalog.
- If a policy or tag is attached a table or view column, dropping the schema successfully requires the policy or tag to be self-contained
  within the database and schema. For example, `database_1` contains `policy_1` and `policy_1` is only used in `database_1`.
  Otherwise, a [dangling reference](/user-guide/database-replication-considerations#label-database-replication-dangling-references) occurs.
- The DROP operation fails if a session policy or password policy is set on a user or the account.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

Important

If the schema contains a snapshot set that has an associated snapshot policy with a retention lock, and there are any
unexpired snapshots in the snapshot set, then you can’t delete the schema containing the snapshot set.
In that case, you must wait for all the snapshots in the set to expire.
This restriction applies even to privileged roles such as ACCOUNTADMIN, and to Snowflake support.
For that reason, be careful when specifying retention lock and a long expiration
period in a snapshot policy.

## Examples

Drop a schema named `myschema` (from the [CREATE SCHEMA](/sql-reference/sql/create-schema) examples):

> Copy code
>
> ```
> DROP SCHEMA myschema;
>
> +--------------------------------+
> | status                         |
> |--------------------------------|
> | MYSCHEMA successfully dropped. |
> +--------------------------------+
>
> SHOW SCHEMAS;
>
> +---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+
> | created_on                      | name               | is_default | is_current | database_name | owner  | comment                                                   | options | retention_time |
> |---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------|
> | Fri, 13 May 2016 17:26:07 -0700 | INFORMATION_SCHEMA | N          | N          | MYTESTDB      |        | Views describing the contents of schemas in this database |         |              1 |
> | Tue, 17 Mar 2015 16:57:04 -0700 | PUBLIC             | N          | Y          | MYTESTDB      | PUBLIC |                                                           |         |              1 |
> +---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+
> ```
