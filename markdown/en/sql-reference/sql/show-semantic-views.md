# SHOW SEMANTIC VIEWS

Lists the [semantic views](/user-guide/views-semantic/overview) for which you have access privileges. You can list
views for the current or specified schema.

The output returns view metadata and properties, ordered lexicographically by database, schema, and semantic view name. This is
important to note if you want to filter the results using the provided filters.

See also:
:   [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) , [ALTER SEMANTIC VIEW](/sql-reference/sql/alter-semantic-view) , [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) , [DROP SEMANTIC VIEW](/sql-reference/sql/drop-semantic-view) , [SHOW SEMANTIC DIMENSIONS](/sql-reference/sql/show-semantic-dimensions) , [SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) , [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts) , [SHOW SEMANTIC METRICS](/sql-reference/sql/show-semantic-metrics)

## Syntax

Copy code

```
SHOW [ TERSE ] SEMANTIC VIEWS [ LIKE '<pattern>' ]
  [ IN
       {
         ACCOUNT                                         |

         DATABASE                                        |
         DATABASE <database_name>                        |

         SCHEMA                                          |
         SCHEMA <schema_name>                            |
         <schema_name>
       }
  ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Returns only a subset of the output columns:

    - `created_on`
    - `name`
    - `kind`

      The `kind` column value is always `SEMANTIC_VIEW`.
    - `database_name`
    - `schema_name`

    Default: No value (all columns are included in the output)

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

The command output provides semantic view properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the semantic view was created. |
| `name` | Name of the semantic view. |
| `kind` | View type. This is always `SEMANTIC_VIEW`.  This column only appears in the output if you specify TERSE. |
| `database_name` | Database in which the semantic view is stored. |
| `schema_name` | Schema in which the semantic view is stored. |
| `comment` | Comment about the semantic view. |
| `owner` | Role that owns the semantic view. |
| `owner_role_type` | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any | Semantic view |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

The following example lists the semantic views in the database that is currently in use:

Copy code

```
SHOW SEMANTIC VIEWS;
```

```
+-------------------------------+----------------------+---------------+-------------+---------+---------+-----------------+-----------+
| created_on                    | name                 | database_name | schema_name | comment | owner   | owner_role_type | extension |
|-------------------------------+----------------------+---------------+-------------+---------+---------+-----------------+-----------+
| 2025-04-10 08:29:02.732 -0700 | MY_SEMANTIC_VIEW_1   | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:29:21.117 -0700 | MY_SEMANTIC_VIEW_2   | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:29:38.040 -0700 | MY_SEMANTIC_VIEW_3   | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:47:33.161 -0700 | MY_SEMANTIC_VIEW_4   | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:47:46.294 -0700 | MY_SEMANTIC_VIEW_5   | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:47:58.480 -0700 | MY_SEMANTIC_VIEW_6   | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-02-28 16:16:04.002 -0800 | O_TPCH_SEMANTIC_VIEW | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-03-21 07:03:54.120 -0700 | TPCH_REV_ANALYSIS    | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
+-------------------------------+----------------------+---------------+-------------+---------+---------+-----------------+-----------+
```

The following example includes only a subset of the output columns:

Copy code

```
SHOW TERSE SEMANTIC VIEWS;
```

```
+-------------------------------+-----------------------+---------------+---------------+-------------------+
| created_on                    | name                  | kind          | database_name | schema_name       |
|-------------------------------+-----------------------+---------------+---------------+-------------------|
| 2025-04-10 08:29:02.732 -0700 | MY_SEMANTIC_VIEW_1    | SEMANTIC_VIEW | MY_DB         | MY_SCHEMA         |
| 2025-04-10 08:29:21.117 -0700 | MY_SEMANTIC_VIEW_2    | SEMANTIC_VIEW | MY_DB         | MY_SCHEMA         |
| 2025-04-10 08:29:38.040 -0700 | MY_SEMANTIC_VIEW_3    | SEMANTIC_VIEW | MY_DB         | MY_SCHEMA         |
| 2025-04-10 08:47:33.161 -0700 | MY_SEMANTIC_VIEW_4    | SEMANTIC_VIEW | MY_DB         | MY_SCHEMA         |
| 2025-04-10 08:47:46.294 -0700 | MY_SEMANTIC_VIEW_5    | SEMANTIC_VIEW | MY_DB         | MY_SCHEMA         |
| 2025-04-10 08:47:58.480 -0700 | MY_SEMANTIC_VIEW_6    | SEMANTIC_VIEW | MY_DB         | MY_SCHEMA         |
| 2025-02-28 16:16:04.002 -0800 | O_TPCH_SEMANTIC_VIEW  | SEMANTIC_VIEW | MY_DB         | MY_SCHEMA         |
| 2025-03-21 07:03:54.120 -0700 | TPCH_REV_ANALYSIS     | SEMANTIC_VIEW | MY_DB         | MY_SCHEMA         |
+-------------------------------+-----------------------+---------------+---------------+-------------------+
```

The following example displays the semantic views with names that have the string `tpch`:

Copy code

```
SHOW SEMANTIC VIEWS LIKE '%tpch%';
```

```
+-------------------------------+----------------------+---------------+-------------+---------+---------+-----------------+-----------+
| created_on                    | name                 | database_name | schema_name | comment | owner   | owner_role_type | extension |
|-------------------------------+----------------------+---------------+-------------+---------+---------+-----------------+-----------|
| 2025-02-28 16:16:04.002 -0800 | O_TPCH_SEMANTIC_VIEW | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-03-21 07:03:54.120 -0700 | TPCH_REV_ANALYSIS    | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
+-------------------------------+----------------------+---------------+-------------+---------+---------+-----------------+-----------+
```

The following example displays the semantic views with names that start with `MY_SEMANTIC_VIEW`:

Copy code

```
SHOW SEMANTIC VIEWS STARTS WITH 'MY_SEMANTIC_VIEW';
```

```
+-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------+
| created_on                    | name               | database_name | schema_name | comment | owner   | owner_role_type | extension |
|-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------|
| 2025-04-10 08:29:02.732 -0700 | MY_SEMANTIC_VIEW_1 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:29:21.117 -0700 | MY_SEMANTIC_VIEW_2 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:29:38.040 -0700 | MY_SEMANTIC_VIEW_3 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:47:33.161 -0700 | MY_SEMANTIC_VIEW_4 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:47:46.294 -0700 | MY_SEMANTIC_VIEW_5 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:47:58.480 -0700 | MY_SEMANTIC_VIEW_6 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
+-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------+
```

The following example displays the first three semantic views with names that start with `MY_SEMANTIC_VIEW`:

Copy code

```
SHOW SEMANTIC VIEWS STARTS WITH 'MY_SEMANTIC_VIEW' LIMIT 3;
```

```
+-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------+
| created_on                    | name               | database_name | schema_name | comment | owner   | owner_role_type | extension |
|-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------|
| 2025-04-10 08:29:02.732 -0700 | MY_SEMANTIC_VIEW_1 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:29:21.117 -0700 | MY_SEMANTIC_VIEW_2 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:29:38.040 -0700 | MY_SEMANTIC_VIEW_3 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
+-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------+
```

The following example displays the three semantic views with names that start with `MY_SEMANTIC_VIEW` after the view named
`MY_SEMANTIC_VIEW_3`:

Copy code

```
SHOW SEMANTIC VIEWS STARTS WITH 'MY_SEMANTIC_VIEW' LIMIT 3 FROM 'MY_SEMANTIC_VIEW_3';
```

```
+-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------+
| created_on                    | name               | database_name | schema_name | comment | owner   | owner_role_type | extension |
|-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------|
| 2025-04-10 08:47:33.161 -0700 | MY_SEMANTIC_VIEW_4 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:47:46.294 -0700 | MY_SEMANTIC_VIEW_5 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
| 2025-04-10 08:47:58.480 -0700 | MY_SEMANTIC_VIEW_6 | MY_DB         | MY_SCHEMA   |         | MY_ROLE | ROLE            | NULL      |
+-------------------------------+--------------------+---------------+-------------+---------+---------+-----------------+-----------+
```
