# SHOW STREAMLITS

Lists the Streamlit objects for which you have access privileges.

See also:
:   [CREATE STREAMLIT](/sql-reference/sql/create-streamlit), [DESCRIBE STREAMLIT](/sql-reference/sql/desc-streamlit), [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit), [DROP STREAMLIT](/sql-reference/sql/drop-streamlit)

## Syntax

Copy code

```
SHOW [ TERSE ] STREAMLITS [ LIKE '<pattern>' ]
                          [ IN
                                {
                                  ACCOUNT                   |

                                  DATABASE                  |
                                  DATABASE <db_name>        |

                                  SCHEMA
                                  SCHEMA <schema_name>      |
                                  <schema_name>             |
                                }
                          ]
                          [ LIMIT <rows> [ FROM '<name_string>' ]
```

## Parameters

`TERSE`
:   Returns only a subset of the output columns:

    - `created_on`
    - `name`
    - `kind`

      The `kind` column value is always Streamlit.
    - `database_name`
    - `schema_name`
    - `title`
    - `url_id`

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

## Access control requirements

If your role does not own the objects in the following table, then your role
must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Streamlit objects that you list | Anyone can execute this command, but only Streamlit objects for which you have USAGE privileges are returned in the output. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can use this command to list Streamlit objects for the current/specified database or schema, or across your entire account.
- The command doesn’t list Streamlit objects that have been dropped.
- The command doesn’t require a running warehouse to run.

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Output

The command output provides Streamlit object properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the Streamlit object was created. |
| `name` | Name of the Streamlit object. |
| `database_name` | Database in which the Streamlit object is stored. |
| `schema_name` | Schema in which the Streamlit object is stored. |
| `title` | Title of the Streamlit app that displays in Snowsight. |
| `comment` | Comment for the Streamlit object. |
| `owner` | Role that owns the Streamlit object. |
| `query_warehouse` | Warehouse where queries issued by the Streamlit application are run. |
| `url_id` | Unique ID associated with the Streamlit object. |
| `owner_role_type` | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more
