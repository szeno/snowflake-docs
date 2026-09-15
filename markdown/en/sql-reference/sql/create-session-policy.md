# CREATE SESSION POLICY

Creates a new session policy or replaces an existing session policy.

A session policy defines the idle session timeout period in minutes. Administrators can optionally set different timeout values for the
Snowflake web interface and other Snowflake clients, and can set a privilege ceiling for agents with
`AGENT_RESTRICTED_SESSION_SCOPE`. For that property, see [Restricted Session Scope for agents](/user-guide/restricted-session-scope).

After creating a session policy, apply the session policy to your Snowflake account using an [ALTER ACCOUNT](/sql-reference/sql/alter-account)
statement or a user using an [ALTER USER](/sql-reference/sql/alter-user) statement.

See also:
:   [Session Policy DDL Reference](/user-guide/session-policies-managing#label-session-policy-ddl-reference)

## Syntax

Copy code

```
CREATE [OR REPLACE] SESSION POLICY [IF NOT EXISTS] <name>
  [ SESSION_IDLE_TIMEOUT_MINS = <integer> ]
  [ SESSION_UI_IDLE_TIMEOUT_MINS = <integer> ]
  [ SESSION_MAX_LIFESPAN_MINS = <integer> ]
  [ SESSION_UI_MAX_LIFESPAN_MINS = <integer> ]
  [ ALLOWED_SECONDARY_ROLES = ( [ { 'ALL' | <role_name> [ , <role_name> ... ] } ] ) ]
  [ BLOCKED_SECONDARY_ROLES = ( [ { 'ALL' | <role_name> [ , <role_name> ... ] } ] ) ]
  [ AGENT_RESTRICTED_SESSION_SCOPE = { '<predefined_scope>' | '<rss_object_name>' | $$ <yaml_definition> $$ } ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Identifier for the session policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`SESSION_IDLE_TIMEOUT_MINS = integer`
:   For Snowflake clients and programmatic clients, the number of minutes in which a session can be idle before users must authenticate to
    Snowflake again. If a value is not specified, Snowflake uses the default value.

    The number of minutes can be any integer between `5` and `1440`, inclusive.

    Default: `240` (4 hours)

`SESSION_UI_IDLE_TIMEOUT_MINS = integer`
:   For Snowsight, the number of minutes in which a session can be idle before a user must authenticate to Snowflake again. If a
    value is not specified, Snowflake uses the default value.

    The number of minutes can be any integer between `5` and `1440`, inclusive.

    Default: `1080` (18 hours)

`SESSION_MAX_LIFESPAN_MINS = integer`
:   For Snowflake clients and programmatic clients, the maximum number of minutes a session can remain active before users must
    authenticate to Snowflake again, regardless of activity. If a value is not specified, Snowflake uses the default value.

    The number of minutes can be any integer between `0` and `43200` (30 days), inclusive. A value of `0` means no maximum
    lifespan is enforced.

    Default: `0` (no maximum lifespan enforcement)

`SESSION_UI_MAX_LIFESPAN_MINS = integer`
:   For Snowsight, the maximum number of minutes a session can remain active before users must authenticate to Snowflake
    again, regardless of activity. If a value is not specified, Snowflake uses the default value.

    The number of minutes can be any integer between `0` and `43200` (30 days), inclusive. A value of `0` means no maximum
    lifespan is enforced.

    Default: `0` (no maximum lifespan enforcement)

`ALLOWED_SECONDARY_ROLES = ( [ { 'ALL' | role_name [ , role_name ... ] } ] )`
:   Specifies the allowed secondary roles for a session policy, if any.

    The possible values for the property are:

    `()`
    :   Disallows secondary roles.

    `('ALL')`
    :   Allows all secondary roles.

    `( role_name [ , role_name ... ] )`
    :   Allows the specified roles as secondary roles. The secondary roles can be user-defined account roles or system roles. Specify the
        role name as it is stored in Snowflake. For details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Default: `('ALL')`. If you do not set the property when you create a new session policy, all secondary roles are allowed.

`BLOCKED_SECONDARY_ROLES = ( [ { 'ALL' | role_name [ , role_name ... ] } ] )`
:   Specifies the blocked secondary roles for a session policy, if any. Blocked secondary roles take precedence over
    allowed secondary roles.

    The possible values for the property are:

    `()`
    :   Allows all secondary roles.

    `('ALL')`
    :   Disallows secondary roles.

    `( role_name [ , role_name ... ] )`
    :   Blocks the specified roles as secondary roles. The specified roles, and the roles granted to those roles, cannot be
        activated as secondary roles. These blocked roles can be user-defined account roles or system roles. Specify the
        role name as it is stored in Snowflake. For details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Default: `()`. If you do not set the property when you create a new session policy, all secondary roles are allowed.

`AGENT_RESTRICTED_SESSION_SCOPE = { '<predefined_scope>' | '<rss_object_name>' | $$ <yaml_definition> $$ }`
:   Privilege ceiling that Snowflake applies when an agent is active in the session
    (`SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')` returns `TRUE`). When no agent is active,
    this property is ignored.

    Specify one of the following:

    - A Snowflake predefined scope name, such as `'SNOWFLAKE$DATA_READ'`.
    - The fully qualified name of a [restricted session scope](/user-guide/restricted-session-scope) object.
    - An inline YAML document that defines the privilege ceiling.

    For predefined scopes, YAML structure, and examples, see [Restricted Session Scope for agents](/user-guide/restricted-session-scope).

`COMMENT = 'string_literal'`
:   Adds a comment or overwrites an existing comment for the session policy.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SESSION POLICY | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on session policy DDL and privileges, see [Managing session policies](/user-guide/session-policies-managing).

## Usage notes

- If you want to replace an existing session policy and need to see the current definition of the policy, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE SESSION POLICY](/sql-reference/sql/desc-session-policy) command.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create a session policy for your current account:

> Copy code
>
> ```
> CREATE SESSION POLICY session_policy_prod_1
>   SESSION_IDLE_TIMEOUT_MINS = 30
>   SESSION_UI_IDLE_TIMEOUT_MINS = 30
>   SESSION_MAX_LIFESPAN_MINS = 480
>   SESSION_UI_MAX_LIFESPAN_MINS = 480
>   COMMENT = 'session policy for use in the prod_1 environment'
> ;
> ```
