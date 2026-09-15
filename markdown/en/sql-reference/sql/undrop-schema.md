# UNDROP SCHEMA

Restore the most recent version of a dropped schema.

See also:
:   [CREATE SCHEMA](/sql-reference/sql/create-schema) , [ALTER SCHEMA](/sql-reference/sql/alter-schema) , [DESCRIBE SCHEMA](/sql-reference/sql/desc-schema) , [DROP SCHEMA](/sql-reference/sql/drop-schema) , [SHOW SCHEMAS](/sql-reference/sql/show-schemas)

## Syntax

Copy code

```
UNDROP SCHEMA <name>
```

## Parameters

`name`
:   Specifies the identifier for the schema to restore. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- A schema can only be restored to the database that contained the schema at the time of its deletion. For example, if you
  create and drop schema `s1` in database `db1`, then change the current database to `db2` and attempt to restore
  schema `s1` by ID (or fully-qualified name, `db1.s1`), schema `s1` is restored in database `db1` rather than in the
  current database, `db2`.
- If a schema with the same name already exists, an error is returned.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

- Hybrid tables that belong to the specified schema are not undropped.
- If you have multiple dropped schemas with the same name, you can use the [IDENTIFIER keyword](/sql-reference/identifier-literal)
  with the system-generated identifier (from the [SCHEMATA view](/sql-reference/account-usage/schemata)) to specify which schema to restore.
  The name of the restored schema remains the same. See [Examples](#examples).

  Note

  You can only use the system-generated identifier with the IDENTIFIER() keyword when executing the UNDROP command for notebooks, tables, block storage snapshots, schemas, and databases.

## Examples

### Basic example

Restore the most recent version of a dropped schema (this example builds on the examples provided for [DROP SCHEMA](/sql-reference/sql/drop-schema)):

Copy code

```
UNDROP SCHEMA myschema;
```

```
+----------------------------------------+
| status                                 |
|----------------------------------------|
| Schema MYSCHEMA successfully restored. |
+----------------------------------------+
```

Copy code

```
SHOW SCHEMAS HISTORY;
```

```
+---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+------------+
| created_on                      | name               | is_default | is_current | database_name | owner  | comment                                                   | options | retention_time | dropped_on |
|---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+------------|
| Fri, 13 May 2016 17:26:07 -0700 | INFORMATION_SCHEMA | N          | N          | MYTESTDB      |        | Views describing the contents of schemas in this database |         |              1 | [NULL]     |
| Tue, 17 Mar 2015 17:18:42 -0700 | MYSCHEMA           | N          | N          | MYTESTDB      | PUBLIC |                                                           |         |              1 | [NULL]     |
| Tue, 17 Mar 2015 16:57:04 -0700 | PUBLIC             | N          | Y          | MYTESTDB      | PUBLIC |                                                           |         |              1 | [NULL]     |
+---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+------------+
```

### UNDROP schema using the schema ID

Restore a dropped schema by ID using IDENTIFIER(). You can find the schema ID of the specific schema to undrop using the `schema_id`
column in the [SCHEMATA view](/sql-reference/account-usage/schemata). For example, if you have multiple dropped schemas named `s1`, and you want
to restore the second-to-last dropped schema `s1`, follow these steps:

1. Find the schema ID of the dropped schema in the Account Usage SCHEMATA view:

   Copy code

   ```
   SELECT schema_id,
     schema_name,
     catalog_name,
     created,
     deleted,
     comment
   FROM SNOWFLAKE.ACCOUNT_USAGE.SCHEMATA
   WHERE schema_name = 'S1'
   AND catalog_name = 'DB1'
   AND deleted IS NOT NULL
   ORDER BY deleted;
   ```

   ```
   +-----------+-------------+---------------+-------------------------------+-------------------------------+---------+
   | SCHEMA_ID | SCHEMA_NAME | CATALOG_NAME  | CREATED                       | DELETED                       | COMMENT |
   |-----------+-------------+---------------+-------------------------------+-------------------------------+---------|
   |       797 | S1          | DB1           | 2024-07-01 17:53:01.955 -0700 | 2024-07-01 17:53:11.889 -0700 | NULL    |
   |       798 | S1          | DB1           | 2024-07-01 17:53:11.889 -0700 | 2024-07-01 17:53:16.327 -0700 | NULL    |
   |       799 | S1          | DB1           | 2024-07-01 17:53:16.327 -0700 | 2024-07-01 17:53:25.066 -0700 | NULL    |
   +-----------+-------------+---------------+-------------------------------+-------------------------------+---------+
   ```
2. Undrop schema `s1` using schema ID. To restore the second-to-last deleted schema, use schema ID `798` from the output of the previous
   statement. After you execute the following statement, the schema is restored with its original name, `s1`:

   Copy code

   ```
   UNDROP SCHEMA IDENTIFIER(798);
   ```
