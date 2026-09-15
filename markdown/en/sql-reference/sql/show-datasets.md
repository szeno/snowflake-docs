# SHOW DATASETS

Displays information about the datasets in your account.
You can show all datasets or use the IN subcommand to only display results at the schema or database level.

See also:
:   [CREATE DATASET](/sql-reference/sql/create-dataset) , [ALTER DATASET](/sql-reference/sql/alter-dataset)

## Syntax

Copy code

```
SHOW DATASETS
  [ LIKE '<pattern>' ]
  [ IN { SCHEMA <schema_name> | DATABASE <db_name> | ACCOUNT } ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Optional parameters

`LIKE pattern`
:   Restricts the list of returned datasets to those matching the specified pattern.

`IN {SCHEMA <schema_name> | DATABASE <db_name> | ACCOUNT}`
:   Restricts the list of returned datasets to those in the specified schema or database within an account.

`DATABASE db_name`
:   Restricts the list of returned datasets to those in the specified database.
    If you specify a database without `db_name` and no database is in use, the keyword has no
    effect on the output.

`SCHEMA schema_name`
:   By default, returns records for the schema in use. You can also specify a `schema_name`.

`STARTS WITH name_string`
:   Uses the string that you specify to limit the datasets returned.
    The names of the datasets returned have the same beginning characters as the specified string.

`LIMIT rows [ FROM name_string ]`
:   Limits the number of returned datasets to the specified number of rows.
    The optional FROM clause specifies the starting point for the returned datasets.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or USAGE | Dataset | Provides the privilege to show the datasets within the account. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example shows two datasets in the PUBLIC schema:

Copy code

```
SHOW DATASETS IN SCHEMA PUBLIC LIMIT 2;
```
