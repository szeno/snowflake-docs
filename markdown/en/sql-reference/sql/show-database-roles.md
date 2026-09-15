# SHOW DATABASE ROLES

Lists all the database roles in the specified database.

Important

A user with any active role that has been granted any privilege on the active database (e.g. USAGE) can list the database roles in the
database. However, this does not necessarily mean the role allows users to use the database roles to perform SQL actions. To use a
database role, it must first be granted to an account role that users can activate in a user session, or to an account role lower in a
hierarchy.

This is a part of Discretionary Access Control and Role-Based Access Control. For more information, see
[Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [SHOW GRANTS](/sql-reference/sql/show-grants) , [CREATE DATABASE ROLE](/sql-reference/sql/create-database-role) , [ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role) , [DROP DATABASE ROLE](/sql-reference/sql/drop-database-role)

## Syntax

Copy code

```
SHOW DATABASE ROLES IN DATABASE <name>
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Required parameters

`name`
:   Specifies the name of the database.

    The command returns an error if you do not specify the name identifier.

## Optional parameters

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

## Usage notes

- This command only supports showing database roles in a specific database.

  You can’t use this command to show database roles in the account.

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

## Example

Return up to ten database roles in the database named `mydb` after the first database role named `db_role2`:

Copy code

```
SHOW DATABASE ROLES IN DATABASE mydb LIMIT 10 FROM 'db_role2';
```
