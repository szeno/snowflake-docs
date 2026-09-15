# SHOW SEMANTIC DIMENSIONS

Lists the dimensions in the [semantic views](/user-guide/views-semantic/overview) for which you have access privileges.

You can use this command to list objects in the current database and schema for the session, a specified database or schema, or
your entire account.

The output includes the metadata and properties for each object. The objects are sorted lexicographically by database, schema,
and object name (see Output in this topic for descriptions of the output columns). The order of rows in the results is important
to note if you want to filter the results.

See also:
:   [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) , [ALTER SEMANTIC VIEW](/sql-reference/sql/alter-semantic-view) , [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) , [DROP SEMANTIC VIEW](/sql-reference/sql/drop-semantic-view) , [SHOW SEMANTIC VIEWS](/sql-reference/sql/show-semantic-views) , [SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) , [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts) , [SHOW SEMANTIC METRICS](/sql-reference/sql/show-semantic-metrics)

## Syntax

Copy code

```
SHOW SEMANTIC DIMENSIONS [ LIKE '<pattern>' ]
                         [ IN
                              {
                                <semantic_view_name>           |

                                ACCOUNT                        |

                                DATABASE                       |
                                DATABASE <db_name>             |

                                SCHEMA                         |
                                SCHEMA <db_name>.<schema_name>
                              }
                         ]
                         [ STARTS WITH '<name_string>' ]
                         [ LIMIT <rows> ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `semantic_view_name`
    :   Returns records for the specified semantic view.

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

    `SCHEMA`, `SCHEMA db_name.schema_name`
    :   Returns records for the current schema in use or a specified schema (`db_name.schema_name`). You must specify the
        fully qualified name of the schema.

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

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `database_name` | Name of the database that contains the semantic view. |
| `schema_name` | Name of the schema that contains the semantic view. |
| `semantic_view_name` | Name of the semantic view that contains the dimension. |
| `table_name` | Name of the logical table for the dimension. |
| `name` | Name of the dimension. |
| `data_type` | Data type of the dimension. |
| `synonyms` | Alternative names or synonyms for the dimension. |
| `comment` | Comment about the dimension. |

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

- Executing the command for schema-level objects only returns an object if the current role also has at least one privilege on the
  parent database and schema.

## Examples

The following example lists the dimensions for semantic views that you have any privilege on. The list includes dimensions in
semantic views in the current schema of the current database.

Copy code

```
SHOW SEMANTIC DIMENSIONS;
```

```
+---------------+-------------+--------------------+------------+-------------------------+-------------+-------------------+--------------------------------+
| database_name | schema_name | semantic_view_name | table_name | name                    | data_type   | synonyms          | comment                        |
|---------------+-------------+--------------------+------------+-------------------------+-------------+-------------------+--------------------------------|
| MY_DB         | MY_SCHEMA   | TPCH_ANALYSIS      | CUSTOMER   | CUSTOMER_COUNTRY_CODE   | VARCHAR(15) | NULL              | NULL                           |
| MY_DB         | MY_SCHEMA   | TPCH_ANALYSIS      | CUSTOMER   | CUSTOMER_MARKET_SEGMENT | VARCHAR(10) | NULL              | NULL                           |
| MY_DB         | MY_SCHEMA   | TPCH_ANALYSIS      | CUSTOMER   | CUSTOMER_NAME           | VARCHAR(25) | NULL              | NULL                           |
| MY_DB         | MY_SCHEMA   | TPCH_ANALYSIS      | CUSTOMER   | CUSTOMER_NATION_NAME    | VARCHAR(25) | NULL              | NULL                           |
| MY_DB         | MY_SCHEMA   | TPCH_ANALYSIS      | CUSTOMER   | CUSTOMER_REGION_NAME    | VARCHAR(25) | NULL              | NULL                           |
| MY_DB         | MY_SCHEMA   | TPCH_ANALYSIS      | NATION     | NATION_NAME             | VARCHAR(25) | NULL              | NULL                           |
| MY_DB         | MY_SCHEMA   | TPCH_ANALYSIS      | ORDERS     | ORDER_DATE              | DATE        | NULL              | NULL                           |
| MY_DB         | MY_SCHEMA   | TPCH_REV_ANALYSIS  | CUSTOMERS  | CUSTOMER_NAME           | VARCHAR(25) | ["customer name"] | Name of the customer           |
| MY_DB         | MY_SCHEMA   | TPCH_REV_ANALYSIS  | ORDERS     | ORDER_DATE              | DATE        | NULL              | Date when the order was placed |
| MY_DB         | MY_SCHEMA   | TPCH_REV_ANALYSIS  | ORDERS     | ORDER_YEAR              | NUMBER(4,0) | NULL              | Year when the order was placed |
+---------------+-------------+--------------------+------------+-------------------------+-------------+-------------------+--------------------------------+
```

The following example lists the dimensions for the semantic view named `tpch_rev_analysis` in the current schema of the current database:

Copy code

```
SHOW SEMANTIC DIMENSIONS IN tpch_rev_analysis;
```

```
+---------------+-------------+--------------------+------------+---------------+-------------+-------------------+--------------------------------+
| database_name | schema_name | semantic_view_name | table_name | name          | data_type   | synonyms          | comment                        |
|---------------+-------------+--------------------+------------+---------------+-------------+-------------------+--------------------------------|
| MY_DB         | MY_SCHEMA   | TPCH_REV_ANALYSIS  | CUSTOMERS  | CUSTOMER_NAME | VARCHAR(25) | ["customer name"] | Name of the customer           |
| MY_DB         | MY_SCHEMA   | TPCH_REV_ANALYSIS  | ORDERS     | ORDER_DATE    | DATE        | NULL              | Date when the order was placed |
| MY_DB         | MY_SCHEMA   | TPCH_REV_ANALYSIS  | ORDERS     | ORDER_YEAR    | NUMBER(4,0) | NULL              | Year when the order was placed |
+---------------+-------------+--------------------+------------+---------------+-------------+-------------------+--------------------------------+
```
