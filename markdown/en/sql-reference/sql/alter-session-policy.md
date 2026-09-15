# ALTER SESSION POLICY

Modifies the properties for an existing session policy.

Any changes made to the session policy properties go into effect when the next SQL query that uses the session policy runs.

See also:
:   [Session Policy DDL Reference](/user-guide/session-policies-managing#label-session-policy-ddl-reference)

## Syntax

Copy code

```
ALTER SESSION POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER SESSION POLICY [ IF EXISTS ] <name> SET
  [ SESSION_IDLE_TIMEOUT_MINS = <integer> ]
  [ SESSION_UI_IDLE_TIMEOUT_MINS = <integer> ]
  [ SESSION_MAX_LIFESPAN_MINS = <integer> ]
  [ SESSION_UI_MAX_LIFESPAN_MINS = <integer> ]
  [ ALLOWED_SECONDARY_ROLES = ( [ { 'ALL' | <role_name> [ , <role_name> ... ] } ] ) ]
  [ BLOCKED_SECONDARY_ROLES = ( [ { 'ALL' | <role_name> [ , <role_name> ... ] } ] ) ]
  [ AGENT_RESTRICTED_SESSION_SCOPE = { '<predefined_scope>' | '<rss_object_name>' | $$ <yaml_definition> $$ } ]
  [ COMMENT = '<string_literal>' ]

ALTER SESSION POLICY [ IF EXISTS ] <name> SET
  TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER SESSION POLICY [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER SESSION POLICY [ IF EXISTS ] <name> UNSET
  [ SESSION_IDLE_TIMEOUT_MINS ]
  [ SESSION_UI_IDLE_TIMEOUT_MINS ]
  [ SESSION_MAX_LIFESPAN_MINS ]
  [ SESSION_UI_MAX_LIFESPAN_MINS ]
  [ ALLOWED_SECONDARY_ROLES ]
  [ BLOCKED_SECONDARY_ROLES ]
  [ AGENT_RESTRICTED_SESSION_SCOPE ]
  [ COMMENT ]
```

## Parameters

`name`
:   Identifier for the session policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the session policy; must be unique for your account.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`SET ...`
:   Specifies one or more parameters to set for the session policy separated by blank spaces, commas, or new lines.

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
    :   Specifies the secondary roles for a session policy, if any.

        The possible values for the property are:

        `()`
        :   Disallows secondary roles.

        `('ALL')`
        :   Allows all secondary roles.

        `( role_name [ , role_name ... ] )`
        :   Allows the specified roles as secondary roles. The secondary roles can be user-defined account roles or system roles. Specify the
            role name as it is stored in Snowflake. For details, see [Identifier requirements](/sql-reference/identifiers-syntax).

        Default: `('ALL')`. If you unset this property, its value in the output of a [DESCRIBE SESSION POLICY](/sql-reference/sql/desc-session-policy) command is `'ALL'`.

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

        Default: `()`. If you unset this property, its value in the output of a [DESCRIBE SESSION POLICY](/sql-reference/sql/desc-session-policy) command is
        `'()'`.

    `AGENT_RESTRICTED_SESSION_SCOPE = { '<predefined_scope>' | '<rss_object_name>' | $$ <yaml_definition> $$ }`
    :   Privilege ceiling that Snowflake applies when an agent is active in the session. When no agent is
        active, this property is ignored. For values and YAML structure, see
        [Restricted Session Scope for agents](/user-guide/restricted-session-scope).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the session policy.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one or more parameters to unset for the session policy, which resets them to the system defaults.

    You can reset multiple properties with a single ALTER statement. Each property must be separated by a comma. When
    resetting a property, specify only the name. Specifying a value for the property will return an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Session policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on session policy DDL and privileges, see [Managing session policies](/user-guide/session-policies-managing).

## Usage notes

- If you want to update an existing session policy and need to see the current definition of the policy, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE SESSION POLICY](/sql-reference/sql/desc-session-policy) command.
- Before executing an ALTER statement, you can execute a DESCRIBE SESSION POLICY statement to determine the attribute values of the policy.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example updates the session policy to have a Snowsight session timeout value of `15` minutes.

Copy code

```
DESC SESSION POLICY session_policy_prod_1;
```

```
+---------------------------------+-----------------------+------------------------+--------------------------+--------------------------------------------------+
| createdOn                       | name                  | sessionIdleTimeoutMins | sessionUIIdleTimeoutMins | comment                                          |
+---------------------------------+-----------------------+------------------------+--------------------------+--------------------------------------------------+
| Mon, 11 Jan 2021 00:00:00 -0700 | session_policy_prod_1 | 30                     | 30                       | session policy for use in the prod_1 environment |
+---------------------------------+-----------------------+------------------------+--------------------------+--------------------------------------------------+
```

Copy code

```
ALTER SESSION POLICY session_policy_prod_1 SET SESSION_UI_IDLE_TIMEOUT_MINS = 15;
```

The following example sets the maximum session lifespan to `480` minutes (8 hours) for all clients.

Copy code

```
ALTER SESSION POLICY session_policy_prod_1 SET
  SESSION_MAX_LIFESPAN_MINS = 480
  SESSION_UI_MAX_LIFESPAN_MINS = 480;
```
