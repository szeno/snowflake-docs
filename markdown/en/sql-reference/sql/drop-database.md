# DROP DATABASE

Removes a database from the system.

See also:
:   [CREATE DATABASE](/sql-reference/sql/create-database) , [ALTER DATABASE](/sql-reference/sql/alter-database) , [DESCRIBE DATABASE](/sql-reference/sql/desc-database) , [SHOW DATABASES](/sql-reference/sql/show-databases) , [UNDROP DATABASE](/sql-reference/sql/undrop-database)

## Syntax

Copy code

```
DROP DATABASE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Parameters

`name`
:   Specifies the identifier for the database to drop. If the identifier contains spaces, special characters, or mixed-case characters,
    the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`CASCADE | RESTRICT`
:   Specifies whether the database can be dropped if foreign keys exist that reference any tables in the database:

    - `CASCADE` drops the database and all objects in the database, including tables with primary/unique keys that are referenced by
      foreign keys in other tables.
    - `RESTRICT` returns a warning about existing foreign key references and does not drop the database.

    Default: `CASCADE`

## Usage notes

- Dropping a database does not permanently remove it from the system. A version of the dropped database is retained in
  [Time Travel](/user-guide/data-time-travel) for the number of days specified by the `DATA_RETENTION_TIME_IN_DAYS` parameter
  for the database:

  1. Within the Time Travel retention period, a dropped database can be restored using the [UNDROP DATABASE](/sql-reference/sql/undrop-database) command.
  2. When the Time Travel retention period ends, the next state for the dropped database depends on whether it is permanent or transient:

     - A permanent database moves into [Fail-safe](/user-guide/data-failsafe). In Fail-safe (7 days), a dropped database can be
       recovered, but only by Snowflake. When the database leaves Fail-safe, it is purged.
     - A transient database has no Fail-safe, so it is purged when it moves out of Time Travel.
  3. Once a dropped database has been purged, it cannot be recovered; it must be recreated.
- Currently, when a database is dropped, the data retention period for child schemas or tables, if explicitly set to be different from the
  retention of the database, is not honored. The child schemas or tables are retained for the same period of time as the database. To honor
  the data retention period for these child objects (schemas or tables), drop them explicitly before you drop the database or
  schema.
- After dropping a database, creating a database with the same name creates a new version of the database. The dropped version of the
  previous database can still be restored using the following method:

  1. Rename the current version of the database to a different name.
  2. Use the [UNDROP DATABASE](/sql-reference/sql/undrop-database) command to restore the previous version.
- If a policy or tag is attached to a table or view column, dropping the database successfully requires the policy or tag to be self-contained
  within the database and schema. For example, `database_1` contains `policy_1` and `policy_1` is only used in `database_1`.
  Otherwise, a [dangling reference](/user-guide/database-replication-considerations#label-database-replication-dangling-references) occurs.
- The DROP operation fails if a session policy or password policy is set on a user or the account.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

Important

If the database contains a snapshot set that has an associated snapshot policy with a retention lock, and there are any
unexpired snapshots in the snapshot set, then you can’t delete the database containing the snapshot set.
In that case, you must wait for all the snapshots in the set to expire.
This restriction applies even to privileged roles such as ACCOUNTADMIN, and to Snowflake support.
For that reason, be careful when specifying retention lock and a long expiration
period in a snapshot policy.

## Database replication usage notes

- You can drop a secondary database at any time. Only the database owner (i.e. the role with the OWNERSHIP privilege on the database) can
  drop the database.
- A primary database cannot be dropped if one or more replicas of the database (i.e. secondary databases) exist. To drop the primary
  database, first promote a secondary database to serve as the primary database, and then drop the former primary database. Alternatively,
  drop all of the secondary databases for the primary database, and then drop the primary database.

  Note that only the database owner can drop the database.

## Examples

> Copy code
>
> ```
> DROP DATABASE mytestdb2;
>
> +---------------------------------+
> | status                          |
> |---------------------------------|
> | MYTESTDB2 successfully dropped. |
> +---------------------------------+
>
> SHOW DATABASES LIKE 'mytestdb2';
>
> +------------+------+------------+------------+--------+-------+---------+---------+----------------+
> | created_on | name | is_default | is_current | origin | owner | comment | options | retention_time |
> |------------+------+------------+------------+--------+-------+---------+---------+----------------|
> +------------+------+------------+------------+--------+-------+---------+---------+----------------+
>
> SHOW DATABASES HISTORY LIKE 'mytestdb2';
>
> +---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+---------------------------------+
> | created_on                      | name      | is_default | is_current | origin | owner  | comment | options | retention_time | dropped_on                      |
> |---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+---------------------------------|
> | Wed, 25 Feb 2015 16:16:54 -0800 | MYTESTDB2 | N          | N          |        | PUBLIC |         |         |              1 | Fri, 13 May 2016 17:35:09 -0700 |
> +---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+---------------------------------+
> ```
