Categories:
:   [Context functions](/sql-reference/functions-context)

# CURRENT\_AVAILABLE\_ROLES

Returns a list of all account-level roles granted to the current user. The list includes all roles that are granted
directly to the user plus all account-level roles lower in the hierarchies of these roles.

See also:
:   [CURRENT\_ROLE](/sql-reference/functions/current_role) , [CURRENT\_SECONDARY\_ROLES](/sql-reference/functions/current_secondary_roles) , [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session)

## Syntax

Copy code

```
CURRENT_AVAILABLE_ROLES()
```

## Arguments

None.

## Returns

Returns a string (VARCHAR) that is a JSON-encoded list of available account-level roles. The returned value can be
passed to the [PARSE\_JSON](/sql-reference/functions/parse_json) function to get a VARIANT that contains a list of all the
available roles.

## Usage notes

- This function returns a list of account-level roles only when queried by a user. This function is not supported in service contexts that
  don’t have an active user. For example, [tasks](/user-guide/tasks-intro) are executed by a system service that is not associated
  with a user. Thus, when this function is queried within a task, it returns an empty list (`[]`).
- This function does not return the names of database roles, application roles, or class instance roles.
- This function does not account for role activation in a session.

  For example, if specifying this function in the conditions of a [masking policy](/user-guide/security-column-intro) or a
  [row access policy](/user-guide/security-row-intro), the policy might inadvertently restrict access.

  If role activation and role hierarchy is necessary in the policy conditions, use [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session).

## Examples

Return the list of roles granted to the current user:

> Copy code
>
> ```
> SELECT CURRENT_AVAILABLE_ROLES();
>
> +----------------------------------------------------------+
> | ROW | CURRENT_AVAILABLE_ROLES()                          |
> +-----+----------------------------------------------------+
> |  1  | [ "PUBLIC", "ANALYST", "DATA_ADMIN", "DATA_USER" ] |
> +-----+----------------------------------------------------+
> ```

Use the PARSE\_JSON function to return a VARIANT and the [FLATTEN](/sql-reference/functions/flatten) function to obtain a single row for each role:

> Copy code
>
> ```
> SELECT INDEX,VALUE,THIS FROM TABLE(FLATTEN(input => PARSE_JSON(CURRENT_AVAILABLE_ROLES())));
>
> +-----+-------+------------------------+---------------------------+
> | ROW | INDEX | VALUE                  | THIS                      |
> +-----+-------+------------------------+---------------------------+
> |   1 |     0 | "PUBLIC"               | [                         |
> |     |       |                        |   "PUBLIC",               |
> |     |       |                        |   "ANALYST",              |
> |     |       |                        |   "DATA_ADMIN",           |
> |     |       |                        |   "DATA_USER"             |
> |     |       |                        | ]                         |
> +-----+-------+------------------------+---------------------------+
> |   2 |     1 | "ANALYST"              | [                         |
> |     |       |                        |   "PUBLIC",               |
> |     |       |                        |   "ANALYST",              |
> |     |       |                        |   "DATA_ADMIN",           |
> |     |       |                        |   "DATA_USER"             |
> |     |       |                        | ]                         |
> +-----+-------+------------------------+---------------------------+
> |   3 |     2 | "DATA_ADMIN"           | [                         |
> |     |       |                        |   "PUBLIC",               |
> |     |       |                        |   "ANALYST",              |
> |     |       |                        |   "DATA_ADMIN",           |
> |     |       |                        |   "DATA_USER"             |
> |     |       |                        | ]                         |
> +-----+-------+------------------------+---------------------------+
> |   4 |     3 | "DATA_USER"            | [                         |
> |     |       |                        |   "PUBLIC",               |
> |     |       |                        |   "ANALYST",              |
> |     |       |                        |   "DATA_ADMIN",           |
> |     |       |                        |   "DATA_USER"             |
> |     |       |                        | ]                         |
> +-----+-------+------------------------+---------------------------+
> ```
