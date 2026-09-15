# ALTER RESTRICTED SESSION SCOPE

Modifies the properties of an existing [restricted session scope](/user-guide/restricted-session-scope).

`RSS` is a shorthand alias for `RESTRICTED SESSION SCOPE`. You can use either form in this
statement.

Any changes to the YAML definition take effect for new agent activity. An RSS that is already
active in a session is immutable for the lifetime of that session.

See also:
:   [CREATE RESTRICTED SESSION SCOPE](/sql-reference/sql/create-restricted-session-scope) ,
    [DROP RESTRICTED SESSION SCOPE](/sql-reference/sql/drop-restricted-session-scope) ,
    [SHOW RESTRICTED SESSION SCOPES](/sql-reference/sql/show-restricted-session-scopes) ,
    [DESCRIBE RESTRICTED SESSION SCOPE](/sql-reference/sql/desc-restricted-session-scope)

## Syntax

Copy code

```
ALTER { RESTRICTED SESSION SCOPE | RSS } [ IF EXISTS ] <name> AS $$
  <yaml_definition>
$$

ALTER { RESTRICTED SESSION SCOPE | RSS } [ IF EXISTS ] <name> ADD AS $$
  <yaml_fragment>
$$

ALTER { RESTRICTED SESSION SCOPE | RSS } [ IF EXISTS ] <name> REMOVE AS $$
  <yaml_fragment>
$$

ALTER { RESTRICTED SESSION SCOPE | RSS } [ IF EXISTS ] <name> SET
  [ COMMENT = '<string_literal>' ]

ALTER { RESTRICTED SESSION SCOPE | RSS } [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Identifier for the restricted session scope to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`AS $$ yaml_definition $$`
:   Replaces the entire YAML privilege ceiling for the restricted session scope. For the YAML
    structure, see [Restricted Session Scope for agents](/user-guide/restricted-session-scope).

`ADD AS $$ yaml_fragment $$`
:   Merges the fragment’s entries into the current definition. Use this form to widen an existing
    ceiling without restating the full YAML.

`REMOVE AS $$ yaml_fragment $$`
:   Removes entries that match the fragment from the current definition. Use this form to narrow an
    existing ceiling without restating the full YAML.

`SET ...`
:   Specifies one or more properties to set for the restricted session scope:

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the restricted session scope.

`UNSET ...`
:   Specifies properties to unset for the restricted session scope, which resets them to the defaults.

    When unsetting a property, specify only the property name. Specifying a value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| MODIFY or OWNERSHIP | Restricted session scope |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Replace the YAML definition of an existing restricted session scope:

Copy code

```
ALTER RESTRICTED SESSION SCOPE mydb.governance.agent_scope AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data read]
      account: [all]
role_scopes:
  blocked_roles: [ACCOUNTADMIN, SYSADMIN, SECURITYADMIN]
  allow_role_switching: false
$$;
```

Widen an existing definition with a partial manifest:

Copy code

```
ALTER RSS analytics_ro ADD AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [usage]
      object_types: [cortex search service]
      databases: [analytics_db]
$$;
```

Narrow an existing definition with a partial manifest:

Copy code

```
ALTER RSS analytics_ro REMOVE AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data write]
      databases: [analytics_db]
$$;
```
