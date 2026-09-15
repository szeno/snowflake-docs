Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)

Returns information about the session in which the function is called.

You can call this function in the following contexts:

- You can call this function directly in the current session.
- You can run a caller’s rights executable (for example, a caller’s rights stored procedure) that calls this function.
- You can run an owner’s rights executable (for example, an owner’s rights stored procedure) that calls this function, provided
  that the owner role has been granted the READ SESSION privilege on the account.

In any other context, the function returns NULL.

See also:
:   [SYS\_CONTEXT](/sql-reference/functions/sys_context) ,
    [SYS\_CONTEXT (SNOWFLAKE$APPLICATION namespace)](/sql-reference/functions/sys_context_snowflake_application) ,
    [SYS\_CONTEXT (SNOWFLAKE$CURRENT namespace)](/sql-reference/functions/sys_context_snowflake_current) ,
    [SYS\_CONTEXT (SNOWFLAKE$ENVIRONMENT namespace)](/sql-reference/functions/sys_context_snowflake_environment) ,
    [SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization) ,
    [Restricted Session Scope for agents](/user-guide/restricted-session-scope)

## Syntax

**Syntax for retrieving properties:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$SESSION' ,
  '<property>'
)
```

**Syntax for calling functions:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$SESSION' ,
  '<function>' , '<argument>' [ , ... ]
)
```

## Arguments

`'SNOWFLAKE$SESSION'`
:   Specifies that you want to retrieve a property or call a function to return information about the session in which the function
    is called.

`'property'`
:   Name of the property that you want to retrieve. You can specify the following properties:

    | Property | Description |
    | --- | --- |
    | `ACTIVE_RESTRICTED_SESSION_SCOPES` | Returns the Restricted Session Scope currently active for the session, so you can confirm what privilege ceiling is in effect without inspecting the session policy that applied it. For details, see [Restricted Session Scope for agents](/user-guide/restricted-session-scope). |
    | `PRINCIPAL_NAME` | Name of the principal (the user, [task](/user-guide/tasks-intro), or [SPCS service](/developer-guide/snowpark-container-services/overview)) that started the session. The name depends on the value of the `PRINCIPAL_TYPE` property:   - If `PRINCIPAL_TYPE` is one of the following values, the value of the `PRINCIPAL_NAME` property is the name of the   user:    - `USER`   - `USER_PERSON`   - `USER_SERVICE`   - `USER_LEGACY_SERVICE` - If `PRINCIPAL_TYPE` is `TASK`, the value is the name of the task. - If `PRINCIPAL_TYPE` is `SNOWSERVICE`, the value is the name of the SPCS service. |
    | `PRINCIPAL_TYPE` | Type of the principal that started the session. This property can have one of the following values:   - `USER` or `USER_suffix`, if a user started the session. `suffix` depends on the type of the user:    - If the user object has no TYPE property, the value is `USER`.   - If the TYPE property is `PERSON`, the value is `USER_PERSON`.   - If the TYPE property is `SERVICE`, the value is `USER_SERVICE`.   - If the TYPE property is `LEGACY_SERVICE`, the value is `USER_LEGACY_SERVICE`. - `TASK`, if a [task](/user-guide/tasks-intro) started the session. - `SNOWSERVICE`, if an [SPCS service](/developer-guide/snowpark-container-services/overview) started the session. |
    | `PRINCIPAL_EMAIL` | Email address that is associated with the principal. If there is no associated email address, the value of this property is NULL. |
    | `PRINCIPAL_DATABASE` | Name of the database containing the object for the principal. For example, if the principal is a task, the value of this property is the name of the database that contains the task.  If the principal is an account-level object (such as a user), the value of this property is NULL. |
    | `PRINCIPAL_SCHEMA` | Name of the schema containing the object for the principal. For example, if the principal is a task, the value of this property is the name of the schema that contains the task.  If the principal is an account-level object (such as a user), the value of this property is NULL. |
    | `ID` | Identifier for the session in which the function was called. |
    | `IP_ADDRESS` | IPv4 address of the client that submitted the request. Equivalent to calling [CURRENT\_IP\_ADDRESS](/sql-reference/functions/current_ip_address). If the client connected over IPv6, this property doesn’t return the IPv6 address. |
    | `IP_ADDRESS_V6` | IPv6 address of the client that submitted the request. If the client connected over IPv4, this property doesn’t return a value. Use this property to retrieve the client’s IPv6 address when IPv6 ingress is enabled on the account. |
    | `ROLE` | Primary role for the session in which the function was called. |
    | `ROLE_TYPE` | Type of the primary role. This property can have one of the following values:   - `ROLE`, if the primary role is an account role. |
    | `ROLE_DATABASE` | Name of the database that contains the database role, if the primary role is a database role. |
    | `SECONDARY_ROLES` | JSON array of the account-level roles activated as secondary roles in the session. The activated roles include roles that are hierarchically under the requested role. For example, suppose that the user executed:  Copy code  ``` USE SECONDARY ROLES ACCOUNTADMIN; ```  The JSON array for this property includes the ACCOUNTADMIN role and the SECURITYADMIN, SYSADMIN, and USERADMIN roles, which are under the ACCOUNTADMIN role. |
    | `WANTED_SECONDARY_ROLES` | JSON array of the account-level roles requested by the user. For example, suppose that the user executed:  Copy code  ``` USE SECONDARY ROLES ACCOUNTADMIN; ```  The JSON array for this property just includes the ACCOUNTADMIN role. |
    | `DATABASE` | Current database in use for the session, if the role that called the function has privileges to access the database. |
    | `SCHEMA` | Current schema in use for the session, if the role that called the function has privileges to access the schema. |
    | `SCHEMAS` | Current [search path](/sql-reference/name-resolution#label-object-name-resolution-search-path) of schemas for the session, if the role that called the function has privileges to access the current database. |
    | `WAREHOUSE` | Current warehouse in use for the session. |

    Expand

    Show lessSee more

`'function'`
:   Name of the function that you want to call. You can call the following functions:

    - [IS\_DATABASE\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_database_role_activated)
    - [IS\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_role_activated)

`'argument' [ , ... ]`
:   Arguments to pass to the function that you want to call.

    [IS\_ROLE\_ACTIVATED](/sql-reference/functions/is_role_activated) accepts one or more role names and returns `'TRUE'` if any of
    the roles is activated. You can specify multiple roles only when each role is a constant value, such as a string literal. When
    the role is an expression that isn’t a constant, you can specify only a single role.

## Returns

The function returns a VARCHAR value or NULL:

- The return value depends on
  [the property that you are retrieving](/sql-reference/functions/sys_context_snowflake_session#label-sys-context-snowflake-session-property) or
  [the function that you are calling](/sql-reference/functions/sys_context_snowflake_session#label-sys-context-snowflake-session-function).
- If you call SYS\_CONTEXT with the SNOWFLAKE$SESSION namespace outside of
  [any of the supported contexts](/sql-reference/functions/sys_context_snowflake_session#label-sys-content-snowflake-session-contexts), the function returns NULL.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), `SYS_CONTEXT('SNOWFLAKE$SESSION', 'ID')` returns `NUMBER` and
`SYS_CONTEXT('SNOWFLAKE$SESSION', 'IS_ROLE_ACTIVATED', '<role>')` returns `BOOLEAN`. Other properties
and functions in this namespace continue to return `VARCHAR`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- To simulate the values of properties and functions in this namespace when testing policies, use the corresponding
  [POLICY\_CONTEXT arguments](/sql-reference/functions/policy_context#label-policy-context-examples). For example, use
  `SNOWFLAKE$SESSION_ROLE` to simulate the `ROLE` property, or `SNOWFLAKE$SESSION_ACTIVATED_ROLES` to simulate the result of
  IS\_ROLE\_ACTIVATED.
- If you are specifying the function call in a double-quoted string in a shell, escape the `$` character with a backslash
  (`\`) so that `$SESSION` is not interpreted as a shell variable.

  For example, if you are using Snowflake CLI and you are
  [specifying the SQL statement as a command-line argument](/developer-guide/snowflake-cli/sql/execute-sql) in double
  quotes:

  Copy code

  ```
  snow sql --query "SELECT SYS_CONTEXT('SNOWFLAKE\$SESSION', 'PRINCIPAL_NAME');"
  ```

## Examples

The following examples demonstrate how to retrieve context information about the session:

- [Retrieving information about the principal](#label-sys-context-snowflake-session-example-principal)
- [Retrieving information about roles](#label-sys-context-snowflake-session-example-roles)
- [Retrieving the current database, schema, search path, and warehouse](#label-sys-context-snowflake-session-example-db)

### Retrieving information about the principal

The following example returns the name and type of the principal that called the function:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'PRINCIPAL_NAME') AS name,
  SYS_CONTEXT('SNOWFLAKE$SESSION', 'PRINCIPAL_TYPE') AS type,
  SYS_CONTEXT('SNOWFLAKE$SESSION', 'PRINCIPAL_EMAIL') AS email;
```

```
+--------------+-------------+---------------------+
| NAME         | TYPE        | EMAIL               |
|--------------+-------------+---------------------|
| MY_USER_NAME | USER_PERSON | my.user@example.com |
+--------------+-------------+---------------------+
```

### Retrieving information about roles

The following example returns the name and type of the primary role in the session where the function was called:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'ROLE') AS role,
  SYS_CONTEXT('SNOWFLAKE$SESSION', 'ROLE_TYPE') AS type;
```

```
+---------+------+
| ROLE    | TYPE |
|---------+------|
| MY_ROLE | ROLE |
+---------+------+
```

The following example uses the ACCOUNTADMIN role as a secondary role. The example then returns the list of requested secondary
roles in the session (ACCOUNTADMIN) and the list of account-level roles that are activated as secondary roles in the session.

The list of activated roles includes roles that are hierarchically under the requested role. Because the ACCOUNTADMIN role is
activated, the list includes SECURITYADMIN, SYSADMIN, and USERADMIN, which are under the ACCOUNTADMIN role.

Copy code

```
USE SECONDARY ROLES ACCOUNTADMIN;

SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'WANTED_SECONDARY_ROLES') AS requested_roles,
  SYS_CONTEXT('SNOWFLAKE$SESSION', 'SECONDARY_ROLES') AS requested_roles_with_child_roles;
```

```
+------------------+---------------------------------------------------------+
| REQUESTED_ROLES  | REQUESTED_ROLES_WITH_CHILD_ROLES                        |
|------------------+---------------------------------------------------------|
| ["ACCOUNTADMIN"] | ["ACCOUNTADMIN","SECURITYADMIN","SYSADMIN","USERADMIN"] |
+------------------+---------------------------------------------------------+
```

### Retrieving the current database, schema, search path, and warehouse

The following example returns the current database, schema, and warehouse in use for the session:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'DATABASE') AS database,
  SYS_CONTEXT('SNOWFLAKE$SESSION', 'SCHEMA') AS schema,
  SYS_CONTEXT('SNOWFLAKE$SESSION', 'WAREHOUSE') AS warehouse;
```

```
+----------+--------+--------------+
| DATABASE | SCHEMA | WAREHOUSE    |
|----------+--------+--------------|
| MY_DB    | PUBLIC | MY_WAREHOUSE |
+----------+--------+--------------+
```

The following example returns a JSON array that contains the search path for the session:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'SCHEMAS');
```

```
+---------------------------------------------+
| SYS_CONTEXT('SNOWFLAKE$SESSION', 'SCHEMAS') |
|---------------------------------------------|
| ["MY_DB.MY_SCHEMA","MY_DB.PUBLIC"]          |
+---------------------------------------------+
```

The following example returns a row for each element in the search path:

Copy code

```
SELECT value::VARCHAR AS path_element
  FROM TABLE(
    FLATTEN(INPUT => PARSE_JSON(SYS_CONTEXT('SNOWFLAKE$SESSION', 'SCHEMAS'))));
```

```
+-----------------------+
| PATH_ELEMENT          |
|-----------------------|
| BOOKS_DB.BOOKS_SCHEMA |
| BOOKS_DB.PUBLIC       |
+-----------------------+
```
