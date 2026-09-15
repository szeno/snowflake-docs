Categories:
:   [Context functions](/sql-reference/functions-context)

# POLICY\_CONTEXT

Simulates the results of a query based on the value of one or more context functions or
[SYS\_CONTEXT](/sql-reference/functions/sys_context) namespace properties, which lets you determine how policies affect query
results. Context functions and SYS\_CONTEXT properties return a value based on the current context of a query: for example, who is
executing the query, which roles are activated, or whether an agent is invoking the query. Policy bodies often use these values to
determine which value to return from the policy.

This function evaluates the following policies to determine the query results:

- [Masking policies](/user-guide/security-column-intro)
- [Row access policies](/user-guide/security-row-intro)
- [Aggregation policies](/user-guide/aggregation-policies)
- [Join policies](/user-guide/join-policies)
- [Projection policies](/user-guide/projection-policies)

## Syntax

Copy code

```
EXECUTE USING
POLICY_CONTEXT(
  <arg> => '<string_literal>'
  [ , <arg> => '<string_literal>' , ... ]
  [ , <arg> => ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
)
AS
SELECT <query>
```

## Arguments

You can specify context function arguments, SYS\_CONTEXT property arguments, or both. You must specify at least one argument.

The following table summarizes all supported arguments:

| Argument | Type | Description |
| --- | --- | --- |
| `CURRENT_USER` | Context function | Current user executing the query |
| `CURRENT_ROLE` | Context function | Current role in use |
| `CURRENT_AVAILABLE_ROLES` | Context function | Available roles for the current user |
| `CURRENT_ACCOUNT` | Context function | Current account |
| `SNOWFLAKE$SESSION_ROLE` | SYS\_CONTEXT property | Primary role for the session |
| `SNOWFLAKE$SESSION_PRINCIPAL_NAME` | SYS\_CONTEXT property | Name of the principal that started the session |
| `SNOWFLAKE$SESSION_PRINCIPAL_TYPE` | SYS\_CONTEXT property | Type of the principal that started the session |
| `SNOWFLAKE$SESSION_DATABASE` | SYS\_CONTEXT property | Current database in use for the session |
| `SNOWFLAKE$SESSION_SCHEMA` | SYS\_CONTEXT property | Current schema in use for the session |
| `SNOWFLAKE$SESSION_WAREHOUSE` | SYS\_CONTEXT property | Current warehouse in use for the session |
| `SNOWFLAKE$SESSION_ACTIVATED_ROLES` | SYS\_CONTEXT list | Set of activated account roles in the session |
| `SNOWFLAKE$SESSION_ACTIVATED_DATABASE_ROLES` | SYS\_CONTEXT list | Set of activated database roles in the session |
| `SNOWFLAKE$CURRENT_ACTIVATED_ROLES` | SYS\_CONTEXT list | Set of activated account roles in the current execution context |
| `SNOWFLAKE$CURRENT_ACTIVATED_DATABASE_ROLES` | SYS\_CONTEXT list | Set of activated database roles in the current execution context |

Expand

Show lessSee more

### Context function arguments

`context_function => 'string_literal'`
:   Specifies a context function and its value as a string.

    Snowflake supports the following context functions and their values as arguments:

    - [CURRENT\_USER](/sql-reference/functions/current_user)
    - [CURRENT\_ROLE](/sql-reference/functions/current_role)
    - [CURRENT\_AVAILABLE\_ROLES](/sql-reference/functions/current_available_roles)
    - [CURRENT\_ACCOUNT](/sql-reference/functions/current_account)

    To determine the format to use as a string value, execute a query using the function. For example:

    > Copy code
    >
    > ```
    > SELECT CURRENT_USER();
    >
    > +----------------+
    > | CURRENT_USER() |
    > |----------------|
    > | JSMITH         |
    > +----------------+
    > ```

    The string value should be `'JSMITH'`.

    Note that if specifying CURRENT\_AVAILABLE\_ROLES and multiple role values, such as `ROLE1` and `ROLE2`, enclose the list of roles in square brackets as follows:

    > `['ROLE1', 'ROLE2']`

### SYS\_CONTEXT property arguments

`sys_context_key => 'string_literal'`
:   Specifies a [SYS\_CONTEXT](/sql-reference/functions/sys_context) namespace property and its simulated value as a string.

    The argument name combines the namespace and property, separated by an underscore. For example, `SNOWFLAKE$SESSION_ROLE`
    corresponds to the `ROLE` property in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session).

    Snowflake supports the following SYS\_CONTEXT property arguments:

    | Argument | Description |
    | --- | --- |
    | `SNOWFLAKE$SESSION_ROLE` | Simulates the value of the `ROLE` property in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session). |
    | `SNOWFLAKE$SESSION_PRINCIPAL_NAME` | Simulates the value of the `PRINCIPAL_NAME` property in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session). |
    | `SNOWFLAKE$SESSION_PRINCIPAL_TYPE` | Simulates the value of the `PRINCIPAL_TYPE` property in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session). |
    | `SNOWFLAKE$SESSION_DATABASE` | Simulates the value of the `DATABASE` property in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session). |
    | `SNOWFLAKE$SESSION_SCHEMA` | Simulates the value of the `SCHEMA` property in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session). |
    | `SNOWFLAKE$SESSION_WAREHOUSE` | Simulates the value of the `WAREHOUSE` property in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session). |

    Expand

    Show lessSee more

### SYS\_CONTEXT list arguments

`sys_context_key => ( 'string_literal' [ , 'string_literal' , ... ] )`
:   Specifies a [SYS\_CONTEXT](/sql-reference/functions/sys_context) namespace property and a list of simulated values.
    Enclose the values in parentheses to form a tuple. You can also specify a single value without parentheses.

    Snowflake supports the following SYS\_CONTEXT list arguments:

    | Argument | Description |
    | --- | --- |
    | `SNOWFLAKE$SESSION_ACTIVATED_ROLES` | Simulates the set of activated account roles in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session). |
    | `SNOWFLAKE$SESSION_ACTIVATED_DATABASE_ROLES` | Simulates the set of activated database roles in the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session). |
    | `SNOWFLAKE$CURRENT_ACTIVATED_ROLES` | Simulates the set of activated account roles in the [SNOWFLAKE$CURRENT namespace](/sql-reference/functions/sys_context_snowflake_current) (the current execution context). |
    | `SNOWFLAKE$CURRENT_ACTIVATED_DATABASE_ROLES` | Simulates the set of activated database roles in the [SNOWFLAKE$CURRENT namespace](/sql-reference/functions/sys_context_snowflake_current) (the current execution context). |

    Expand

    Show lessSee more

`query`
:   Specifies the SQL expression to query one or more tables or views.

    Required.

## Usage notes

- This function requires the following:

  - At least one argument that specifies a supported context function or SYS\_CONTEXT property and its value.
  - If a table is protected by a policy, the specified user or role must be granted the following privileges:
    - OWNERSHIP on the table or view, and
    - The APPLY privilege for the policy, either at the account level or on the policy itself:
      - APPLY MASKING POLICY on ACCOUNT or APPLY on MASKING POLICY `policy_name`
      - APPLY ROW ACCESS POLICY on ACCOUNT or APPLY on ROW ACCESS POLICY `policy_name`
      - APPLY AGGREGATION POLICY on ACCOUNT or APPLY on AGGREGATION POLICY `policy_name`
      - APPLY JOIN POLICY on ACCOUNT or APPLY on JOIN POLICY `policy_name`
      - APPLY PROJECTION POLICY on ACCOUNT or APPLY on PROJECTION POLICY `policy_name`
- Snowflake returns an error message if any of the following conditions are true:

  - Using one or more unsupported arguments. Snowflake only supports the arguments listed in the [Arguments](#arguments) section.
  - Not specifying a value properly, including using a string for a value that does not exist
    (for example, no account, user, or role).
  - The SELECT `query` expression does not query a table or view properly (for example, not specifying a table or view at all).
  - Certain data sharing use cases (see the next bullet).
- Data sharing:

  - A data sharing consumer cannot use this function to simulate query results on tables or views that were made available by the data
    sharing provider.

    Additionally, if the consumer `query` expression includes a table or view made available through
    [Secure Data Sharing](/user-guide/data-sharing-intro) and another table or view in the consumer account not associated with the
    data sharing provider account (that is, their own table or view), Snowflake returns an error message.
  - A data sharing provider account can simulate how a data sharing consumer account views tables or views made available through a share.

    To do this, the data sharing provider specifies the consumer account name as the argument. For example:

    Copy code

    ```
    execute using policy_context(current_account => '<consumer_account_name>') ... ;
    ```
- The result depends on the following:

  - The masking policy or projection policy that is set on a column, if any.
  - The row access policy, aggregation policy, or join policy that is set on the table or view, if any.
  - The policy definitions.
  - The `query` expression.
  - The privileges granted to roles.
  - The roles granted to users (including role hierarchy).
  - The arguments in this function.

  Important

  If the result from this function is not what you expected:

  - Consult with your internal policy administrator to determine which tables, views, and columns are protected by policies, and
    to better understand the body definitions of those policies. This administrator might have a custom role like `POLICY_ADMIN`,
    `MASKING_ADMIN`, or `RAP_ADMIN`.
  - Double-check the:
    - Function string values.
    - `SELECT` `query` expression.
    - Privileges [granted to roles](/sql-reference/sql/grant-privilege)
      (for example, SELECT on table or view, USAGE or any other privilege on parent database and schema) and the corresponding
      [privilege inheritance](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance).
    - [Role hierarchy](/user-guide/security-access-control-configure#label-security-role-hierarchy), especially if specifying the CURRENT\_AVAILABLE\_ROLES function and its values
      as an argument for this function.

  Update the SQL statement using this function, as needed, and try again.
- [SYS\_CONTEXT list arguments](#label-policy-context-sys-context-list-args) accept either a single string value or a
  parenthesized tuple of string values. For example, both of the following are valid:

  Copy code

  ```
  -- Single value (no parentheses needed):
  SNOWFLAKE$SESSION_ACTIVATED_ROLES => 'ANALYST'

  -- Multiple values (parenthesized tuple):
  SNOWFLAKE$SESSION_ACTIVATED_ROLES => ('ANALYST', 'PUBLIC')
  ```
- You can combine context function arguments and SYS\_CONTEXT arguments in the same POLICY\_CONTEXT call.
- For more information about the SNOWFLAKE$CURRENT namespace properties that some of these arguments simulate, see
  [SYS\_CONTEXT (SNOWFLAKE$CURRENT namespace)](/sql-reference/functions/sys_context_snowflake_current).

## Examples

Simulate the effect of the PUBLIC system role querying the table `empl_info`:

> Copy code
>
> ```
> EXECUTE USING POLICY_CONTEXT(CURRENT_ROLE => 'PUBLIC')
>   AS SELECT * FROM empl_info;
> ```

Simulate a specific set of activated roles in the session:

> Copy code
>
> ```
> EXECUTE USING POLICY_CONTEXT(
>   SNOWFLAKE$SESSION_ACTIVATED_ROLES => ('ANALYST', 'PUBLIC')
> )
>   AS SELECT * FROM empl_info;
> ```

Combine context function arguments with SYS\_CONTEXT arguments:

> Copy code
>
> ```
> EXECUTE USING POLICY_CONTEXT(
>   CURRENT_ROLE => 'ANALYST',
>   SNOWFLAKE$SESSION_ACTIVATED_ROLES => ('ANALYST', 'PUBLIC'),
>   SNOWFLAKE$CURRENT_ACTIVATED_ROLES => ('ANALYST')
> )
>   AS SELECT * FROM empl_info;
> ```
