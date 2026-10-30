Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION\_SHARING namespace)

Returns consumer identity information that you can use in row access policies and masking
policies on data that you share with accounts in your organization.

By default, identity context functions return NULL when they are evaluated across a share.
The `SNOWFLAKE$ORGANIZATION_SHARING` namespace deliberately exposes selected consumer identity
values for consumer accounts that belong to the same organization as the provider, so that you can
enforce account-aware, principal-aware, and role-aware governance on shared data. The consumer can
be your own account or another account in your organization.

`SYS_CONTEXT` is a framework of functions grouped into namespaces. The `ORGANIZATION` part of the
namespace name means that the values are returned only for consumers in your organization. You
don’t need to add an organization check to your policies: if the consumer account is outside the
provider’s organization, the namespace doesn’t return consumer identity values, so conditions that
depend on them never pass and the data stays masked or filtered.

## Use cases

Use this namespace when you share data with other accounts in your organization and want policies
that target the consumer’s account roles. Consumer identity forms a hierarchy—account, then user,
then role—so you can choose how narrowly a policy targets consumers:

| Target | Use | Example |
| --- | --- | --- |
| Everyone in a consumer account | `CONSUMER_ACCOUNT` | [Multi-tenant row access policy](#label-sys-context-org-sharing-ex-tenant) |
| A specific user | `CONSUMER_SESSION_PRINCIPAL_NAME` | [Principal-based visibility](#label-sys-context-org-sharing-ex-principal) |
| Users with a specific role | `CONSUMER_CURRENT_ROLE` or `IS_CONSUMER_CURRENT_ROLE_ACTIVATED` | [Role-based masking](#label-sys-context-org-sharing-ex-role-mask) and [role-based row access](#label-sys-context-org-sharing-ex-role-rap) |

Expand

Show lessSee more

To target more narrowly, combine levels in one policy—for example, a specific user who also has a
specific role active.

Because the namespace works the same way for your own account and for other accounts in your
organization, you can write one policy for both. For example, if your account and a consumer
account both have an `ANALYST` role, a single masking policy that checks for `ANALYST` applies to
both, so you don’t need separate policies for same-account access and cross-account sharing.

To target consumers with a policy, you must already know the names of their account roles, users,
or account. Snowflake doesn’t list consumer roles to providers. To find the values, ask the
consumer to run the [query that inspects consumer identity](#label-sys-context-org-sharing-ex-inspect).

If you manage access centrally with organization user groups instead of account roles, use the
[SYS\_CONTEXT (SNOWFLAKE$ORGANIZATION namespace)](/sql-reference/functions/sys_context_snowflake_organization) namespace, which provides functions
such as [IS\_GROUP\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_group_activated).

## Supported access

These properties and functions work in row access policies and masking policies for:

- Same-account tables and views
- Direct shares to accounts in your organization
- Private listings targeted to accounts in your organization
- Mountless organization listings

For more information about organization listings, see
[About organizational listings](/user-guide/collaboration/listings/organizational/org-listing-about).

## Syntax

**Syntax for retrieving properties:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$ORGANIZATION_SHARING' ,
  '<property>'
)
```

**Syntax for calling functions:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$ORGANIZATION_SHARING' ,
  '<function>' , '<argument>' [ , ... ]
)
```

## Arguments

`'SNOWFLAKE$ORGANIZATION_SHARING'`
:   Specifies that you want to retrieve consumer identity context for consumers in your
    organization, whether the consumer is your own account or another account in your organization.

`'property'` or `'function'`
:   Name of the property or function that you want to retrieve or call. You can specify the following
    properties and functions:

    | Property | Kind | Arguments | Returns |
    | --- | --- | --- | --- |
    | `CONSUMER_CURRENT_ROLE` | Property | None | The consumer’s effective primary role name. |
    | `CONSUMER_ACCOUNT` | Property | None | The current account identifier, matching [CURRENT\_ACCOUNT](/sql-reference/functions/current_account). |
    | `CONSUMER_SESSION_PRINCIPAL_NAME` | Property | None | The session principal name, mirroring `SYS_CONTEXT('SNOWFLAKE$SESSION', 'PRINCIPAL_NAME')`: the user currently logged in to the consumer account. |
    | `IS_CONSUMER_CURRENT_ROLE_ACTIVATED` | Function | One or more role names (variadic) | TRUE if any of the named roles is active in the consumer’s session; otherwise FALSE. An unknown role name doesn’t match. |

    Expand

    Show lessSee more

`'argument' [ , ... ]`
:   Arguments to pass when you call a function. For `IS_CONSUMER_CURRENT_ROLE_ACTIVATED`, specify one
    or more role names.

## Returns

The function returns a VARCHAR value, a BOOLEAN value, or NULL:

- Property values are returned as VARCHAR (or NULL).
- `IS_CONSUMER_CURRENT_ROLE_ACTIVATED` returns BOOLEAN.

## Usage notes

- Use these properties and functions in row access policies and masking policies on same-account
  objects, shared tables and views, and mountless organization listings within your organization.
- If you specify the function call in a double-quoted string in a shell, escape the `$` character
  with a backslash (`\`) so that `$ORGANIZATION_SHARING` isn’t interpreted as a shell variable.

  For example, if you are using Snowflake CLI:

  Copy code

  ```
  snow sql --query "SELECT SYS_CONTEXT('SNOWFLAKE\$ORGANIZATION_SHARING', 'CONSUMER_CURRENT_ROLE');"
  ```
- You can simulate these values with [POLICY\_CONTEXT](/sql-reference/functions/policy_context) by using the
  corresponding simulation keys:

  - `SNOWFLAKE$ORGANIZATION_SHARING_CONSUMER_CURRENT_ROLE`
  - `SNOWFLAKE$ORGANIZATION_SHARING_CONSUMER_ACCOUNT`
  - `SNOWFLAKE$ORGANIZATION_SHARING_CONSUMER_SESSION_PRINCIPAL_NAME`
  - `SNOWFLAKE$ORGANIZATION_SHARING_CONSUMER_ACTIVATED_ROLES`

## Examples

### Masking policy: role-based masking

Unmask a column only when the consumer’s active primary role is `ANALYST`. Because the policy
checks only the role name, it applies to users with an `ANALYST` role in your own account and in
other accounts in your organization:

Copy code

```
CREATE MASKING POLICY unmask_for_analyst AS (val STRING) RETURNS STRING ->
  CASE
    WHEN UPPER(SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SHARING', 'CONSUMER_CURRENT_ROLE')) = 'ANALYST'
    THEN val
    ELSE '***MASKED***'
  END;
```

### Row access policy: role-based access control

Return rows only when the consumer has either the `DATA_STEWARD` or `AUDITOR` role activated:

Copy code

```
CREATE ROW ACCESS POLICY rap_privileged_roles AS (id INT) RETURNS BOOLEAN ->
  SYS_CONTEXT(
    'SNOWFLAKE$ORGANIZATION_SHARING',
    'IS_CONSUMER_CURRENT_ROLE_ACTIVATED',
    'DATA_STEWARD',
    'AUDITOR'
  );
```

### Multi-tenant row access policy

Return each row only to the consumer account that is allowed to see it, based on the value in the
`allowed_account` column:

Copy code

```
CREATE ROW ACCESS POLICY rap_by_tenant AS (allowed_account STRING) RETURNS BOOLEAN ->
  UPPER(allowed_account)
    = UPPER(SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SHARING', 'CONSUMER_ACCOUNT'));
```

### Masking policy: principal-based visibility

Unmask a column only for specific session principals, such as a service user or platform identity:

Copy code

```
CREATE MASKING POLICY unmask_for_principal AS (val STRING) RETURNS STRING ->
  CASE
    WHEN UPPER(SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SHARING', 'CONSUMER_SESSION_PRINCIPAL_NAME'))
         IN ('ACME_ETL_SVC', 'DATA_PLATFORM')
    THEN val
    ELSE '***MASKED***'
  END;
```

### Masking policy: combine principal and role

Unmask a column only when a specific user also has a specific role active:

Copy code

```
CREATE MASKING POLICY unmask_for_svc_with_role AS (val STRING) RETURNS STRING ->
  CASE
    WHEN UPPER(SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SHARING', 'CONSUMER_SESSION_PRINCIPAL_NAME')) = 'ACME_ETL_SVC'
     AND SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SHARING', 'IS_CONSUMER_CURRENT_ROLE_ACTIVATED', 'ETL_READER')
    THEN val
    ELSE '***MASKED***'
  END;
```

### Inspect consumer identity in the current session

Run this query to see the values that the namespace returns in your current session, without
creating a policy. Use it as a dry run: a provider can ask a consumer to run it with the role
that they will use to query the shared data, and then use the returned values in policies.

Copy code

```
SELECT
  SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SHARING', 'CONSUMER_CURRENT_ROLE') AS consumer_role,
  SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SHARING', 'CONSUMER_ACCOUNT') AS consumer_account,
  SYS_CONTEXT('SNOWFLAKE$ORGANIZATION_SHARING', 'CONSUMER_SESSION_PRINCIPAL_NAME') AS consumer_principal,
  SYS_CONTEXT(
    'SNOWFLAKE$ORGANIZATION_SHARING',
    'IS_CONSUMER_CURRENT_ROLE_ACTIVATED',
    'ANALYST'
  ) AS is_analyst_activated;
```

## Limitations

- Return values aren’t supported for external shares and intra-organization resharing chains.
- Database roles aren’t detected. `CONSUMER_CURRENT_ROLE` returns NULL for database roles and other
  non-standard role types.
