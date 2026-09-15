# DROP TABLE

Removes a table from the current or specified schema, but retains a version of the table so that it can be recovered by using
[UNDROP TABLE](/sql-reference/sql/undrop-table). For information, see [Usage Notes](#usage-notes).

See also:
:   [CREATE TABLE](/sql-reference/sql/create-table) , [ALTER TABLE](/sql-reference/sql/alter-table) , [SHOW TABLES](/sql-reference/sql/show-tables) , [TRUNCATE TABLE](/sql-reference/sql/truncate-table) , [DESCRIBE TABLE](/sql-reference/sql/desc-table)

## Syntax

Copy code

```
DROP TABLE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ]
```

## Parameters

`name`
:   Specifies the identifier for the table to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive
    (for example, `"My Object"`).

    If the table identifier is not fully-qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the command looks for the table in the current schema for the session.

`CASCADE | RESTRICT`
:   Specifies whether the table can be dropped if foreign keys exist that reference the table:

    - CASCADE: Drops the table even if the table has primary or unique keys that are referenced by foreign keys in other tables.
    - RESTRICT: Returns a warning about existing foreign key references and doesn’t drop the table.

    Default: CASCADE for standard tables; RESTRICT for hybrid tables. See also [Dropping hybrid tables](#label-dropping-hybrid-tables).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Dropping a table does not permanently remove it from the system. A version of the dropped table is retained in
  [Time Travel](/user-guide/data-time-travel) for the number of days specified by the
  [data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period) for the table:

  > - Within the Time Travel retention period, you can restore a dropped table by using the [UNDROP TABLE](/sql-reference/sql/undrop-table) command.
  > - Changing the Time Travel retention period for the account or for a parent object (a database or a schema) *after*
  >   you drop a table doesn’t change the Time Travel retention period for the dropped table.
  >   For more information, see the [note in the Time Travel topic](/user-guide/data-time-travel#label-data-retention-for-dropped-table).
  > - When the Time Travel retention period ends, the next state for the dropped table depends on whether it is permanent, transient, or
  >   temporary:
  >   - A permanent table moves into [Fail-safe](/user-guide/data-failsafe). In Fail-safe (7 days), a dropped table can be recovered,
  >     but only by Snowflake. When the table leaves Fail-safe, it is purged.
  >   - A transient or temporary table has no Fail-safe, so it is purged when it moves out of Time Travel.
  >
  >     Note
  >
  >     A long-running Time Travel query delays the movement of any data and objects (tables, schemas, and databases) in the account into
  >     Fail-safe, until the query completes. The purging of temporary and transient tables is delayed in the same way.
  >   - After a dropped table is purged, it can’t be recovered; it must be recreated.
- After you drop a table, creating a table with the same name creates a new version of the table. You can still restore the dropped version of the
  previous table by following these steps:

  1. Rename the current version of the table.
  2. Use the [UNDROP TABLE](/sql-reference/sql/undrop-table) command to restore the previous version of the table.
- Before dropping a table, verify that *no views reference the table*. Dropping a table referenced by a view invalidates the view
  (that is, querying the view returns an “object does not exist” error).
- To drop a table, you must use a role that has OWNERSHIP privilege on the table.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Dropping hybrid tables

When you drop a hybrid table without specifying the RESTRICT or CASCADE option, and the hybrid table
has a primary-key/foreign-key or unique-key/foreign-key relationship with another table, the DROP TABLE
command fails with an error. The default behavior is RESTRICT.

For example:

Copy code

```
CREATE OR REPLACE HYBRID TABLE ht1(
  col1 NUMBER(38,0) NOT NULL,
  col2 NUMBER(38,0) NOT NULL,
  CONSTRAINT pkey_ht1 PRIMARY KEY (col1, col2));

CREATE OR REPLACE HYBRID TABLE ht2(
  cola NUMBER(38,0) NOT NULL,
  colb NUMBER(38,0) NOT NULL,
  colc NUMBER(38,0) NOT NULL,
  CONSTRAINT pkey_ht2 PRIMARY KEY (cola),
  CONSTRAINT fkey_ht1 FOREIGN KEY (colb, colc) REFERENCES ht1(col1,col2));

DROP TABLE ht1;
```

```
SQL compilation error:
Cannot drop the table because of dependencies
```

The DROP TABLE command fails in this case. If necessary, you can override the default behavior by specifying
CASCADE in the DROP TABLE command.

Copy code

```
DROP TABLE ht1 CASCADE;
```

Alternatively in this case, you could drop the dependent table `ht2` first, then drop table `ht1`.

## Examples

Drop a table:

> Copy code
>
> ```
> SHOW TABLES LIKE 't2%';
>
> +---------------------------------+------+---------------+-------------+-----------+------------+------------+------+-------+--------------+----------------+
> | created_on                      | name | database_name | schema_name | kind      | comment    | cluster_by | rows | bytes | owner        | retention_time |
> |---------------------------------+------+---------------+-------------+-----------+------------+------------+------+-------+--------------+----------------+
> | Tue, 17 Mar 2015 16:48:16 -0700 | T2   | TESTDB        | PUBLIC      | TABLE     |            |            |    5 | 4096  | PUBLIC       |              1 |
> +---------------------------------+------+---------------+-------------+-----------+------------+------------+------+-------+--------------+----------------+
>
> DROP TABLE t2;
>
> +--------------------------+
> | status                   |
> |--------------------------|
> | T2 successfully dropped. |
> +--------------------------+
>
> SHOW TABLES LIKE 't2%';
>
> +------------+------+---------------+-------------+------+---------+------------+------+-------+-------+----------------+
> | created_on | name | database_name | schema_name | kind | comment | cluster_by | rows | bytes | owner | retention_time |
> |------------+------+---------------+-------------+------+---------+------------+------+-------+-------+----------------|
> +------------+------+---------------+-------------+------+---------+------------+------+-------+-------+----------------+
> ```

Drop the table again, but don’t raise an error if the table does not exist:

> Copy code
>
> ```
> DROP TABLE IF EXISTS t2;
>
> +------------------------------------------------------------+
> | status                                                     |
> |------------------------------------------------------------|
> | Drop statement executed successfully (T2 already dropped). |
> +------------------------------------------------------------+
> ```
