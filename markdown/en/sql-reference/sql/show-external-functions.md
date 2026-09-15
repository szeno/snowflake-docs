# SHOW EXTERNAL FUNCTIONS

Lists all the external functions created for your account.

For more information, see [Writing external functions](/sql-reference/external-functions).

See also:
:   [SHOW FUNCTIONS](/sql-reference/sql/show-functions) ,
    [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions),
    [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) ,
    [ALTER FUNCTION](/sql-reference/sql/alter-function)

## Syntax

Copy code

```
SHOW EXTERNAL FUNCTIONS [ LIKE '<pattern>' ]
           [ IN { APPLICATION <application_name> | APPLICATION PACKAGE <application_package_name> }  ]
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

    `APPLICATION application_name`, `APPLICATION PACKAGE application_package_name`
    :   Returns records for the named Snowflake Native App or application package.

## Usage notes

- The commands [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions) also display information
  about external functions.

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

## Examples

Show all external functions:

> Copy code
>
> ```
> SHOW EXTERNAL FUNCTIONS;
> ```

Show only external functions matching the specified regular expression:

> Copy code
>
> ```
> SHOW EXTERNAL FUNCTIONS LIKE 'SQUARE%';
> ```
