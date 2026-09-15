# SHOW ROLES

Lists all the roles which you can view across your entire account, including the system-defined roles and any custom roles that exist.

Important

Snowflake allows users to list roles; however, the ability to list roles is not the same as using any role. Knowing the names of
roles does not allow any additional access.

This is a part of Discretionary Access Control and Role-Based Access Control. For more information, see
[Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [SHOW GRANTS](/sql-reference/sql/show-grants) , [CREATE ROLE](/sql-reference/sql/create-role) , [ALTER ROLE](/sql-reference/sql/alter-role) , [DROP ROLE](/sql-reference/sql/drop-role)

## Syntax

Copy code

```
SHOW [ TERSE ] ROLES
  [ LIKE '<pattern>' ]
  [ IN CLASS <class_name> ]
  [ STARTS WITH '<name_string>']
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Returns only a subset of columns:

    `is_default`
    :   Specifies whether the role used to run the command is the user’s default role.

    `is_current`
    :   Specifies whether the role used to run the command is the user’s current role.

    `is_inherited`
    :   Specifies whether the role used to run the command inherits the specified role.

    `is_from_organization_user_group`
    :   If TRUE, the role was imported from an [organization user group](/user-guide/organization-users#label-org-users-groups).

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN CLASS class_name`
:   Returns records for the specified class (`class_name`).

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

## Usage notes

- If you specify `CLASS`, only the following columns are returned:

  ```
  | created_on | name | comment |
  ```

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

## Examples

Show all roles:

> Copy code
>
> ```
> SHOW ROLES;
> ```
>
> ```
> ---------------------------------+---------------+------------+------------+--------------+-------------------+------------------+---------------+---------------+--------------------------+
>            created_on            |     name      | is_default | is_current | is_inherited | assigned_to_users | granted_to_roles | granted_roles |     owner     |         comment          |
> ---------------------------------+---------------+------------+------------+--------------+-------------------+------------------+---------------+---------------+--------------------------+
>  Fri, 05 Dec 2014 16:25:06 -0800 | ACCOUNTADMIN  | Y          | Y          | N            | 1                 | 0                | 2             |               |                          |
>  Mon, 15 Dec 2014 17:58:33 -0800 | ANALYST       | N          | N          | N            | 0                 | 6                | 0             | SECURITYADMIN | Data analyst             |
>  Fri, 05 Dec 2014 16:25:06 -0800 | PUBLIC        | N          | N          | Y            | 0                 | 0                | 0             |               |                          |
>  Fri, 05 Dec 2014 16:25:06 -0800 | SECURITYADMIN | N          | N          | Y            | 0                 | 1                | 0             |               |                          |
>  Fri, 05 Dec 2014 16:25:06 -0800 | SYSADMIN      | N          | N          | Y            | 5                 | 1                | 2             |               |                          |
> ---------------------------------+---------------+------------+------------+--------------+-------------------+------------------+---------------+---------------+--------------------------+
> ```

In this example:

- The ACCOUNTADMIN system-defined role is the current role and default role for the current (i.e. logged-in) user.
- In addition to the four system-defined roles, one custom role (ANALYST) has been created. The role is owned by the SECURITYADMIN
  system-defined role.

Return up to ten account roles in the account after the first role named `my_role2`:

Copy code

```
SHOW ROLES LIMIT 10 FROM 'my_role2';
```
