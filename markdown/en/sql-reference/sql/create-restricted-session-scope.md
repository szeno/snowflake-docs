# CREATE RESTRICTED SESSION SCOPE

Creates a new [restricted session scope](/user-guide/restricted-session-scope) (RSS).

`RSS` is a shorthand alias for `RESTRICTED SESSION SCOPE`. You can use either form in this
statement.

An RSS is a YAML privilege ceiling that limits what an agent can do on behalf of a user. After you
create the object, reference it from a session policy with `AGENT_RESTRICTED_SESSION_SCOPE`.

This command supports the following variants:

- [CREATE OR ALTER RESTRICTED SESSION SCOPE](#label-create-or-alter-restricted-session-scope): Creates a restricted session scope if it
  doesn’t exist, or replaces the definition of an existing restricted session scope. Use this
  variant to replace a definition: `CREATE RESTRICTED SESSION SCOPE` doesn’t support an `OR REPLACE`
  clause.

See also:
:   [ALTER RESTRICTED SESSION SCOPE](/sql-reference/sql/alter-restricted-session-scope) ,
    [DROP RESTRICTED SESSION SCOPE](/sql-reference/sql/drop-restricted-session-scope) ,
    [SHOW RESTRICTED SESSION SCOPES](/sql-reference/sql/show-restricted-session-scopes) ,
    [DESCRIBE RESTRICTED SESSION SCOPE](/sql-reference/sql/desc-restricted-session-scope)

## Syntax

Copy code

```
CREATE { RESTRICTED SESSION SCOPE | RSS } [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
  AS $$
    <yaml_definition>
  $$
```

## Variant syntax

### CREATE OR ALTER RESTRICTED SESSION SCOPE

Creates a new restricted session scope if it doesn’t already exist, or replaces the YAML definition
of an existing restricted session scope.

Copy code

```
CREATE OR ALTER { RESTRICTED SESSION SCOPE | RSS } <name>
  [ COMMENT = '<string_literal>' ]
  AS $$
    <yaml_definition>
  $$
```

## Required parameters

`name`
:   String that specifies the identifier for the restricted session scope; must be unique for the schema
    in which the object is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`AS $$ yaml_definition $$`
:   YAML document that defines the privilege ceiling. The document has two top-level sections:
    `privilege_scopes` (allowed operations and the containers they apply to) and `role_scopes` (roles
    that can be activated while an agent is active).

    For the YAML structure, predefined scopes, and group privileges, see
    [Restricted Session Scope for agents](/user-guide/restricted-session-scope).

## Optional parameters

`COMMENT = 'string_literal'`
:   Adds a comment or overwrites an existing comment for the restricted session scope.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| CREATE RESTRICTED SESSION SCOPE | Schema |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- An RSS is a ceiling on the user’s existing RBAC privileges. It never grants additional privileges.
- If you later update the RSS object, session policies that reference it pick up the change for new
  agent activity. An RSS that is already active in a session is immutable for the lifetime of that
  session.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a restricted session scope that allows account-wide data read, writes only in a sandbox
database, and blocks privileged roles while an agent is active:

Copy code

```
CREATE RESTRICTED SESSION SCOPE mydb.governance.agent_scope AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, program usage]
      account: [all]
    - privileges: [data write]
      databases: [SANDBOX_DB, USER$]
role_scopes:
  blocked_roles: [ACCOUNTADMIN, SYSADMIN, SECURITYADMIN]
  allow_role_switching: false
$$;
```
