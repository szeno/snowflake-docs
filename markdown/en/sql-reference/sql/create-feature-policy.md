# CREATE FEATURE POLICY

Creates a new feature policy. Feature policies can be applied to all databases or a specific database, to all [personal databases](/user-guide/personal-databases#label-personal-databases-feature-policies), or to all [native apps](/developer-guide/native-apps/ui-consumer-feature-policies) or a specific application. For an overview, see [Feature policies](/user-guide/feature-policies).

See also:
:   [ALTER FEATURE POLICY](/sql-reference/sql/alter-feature-policy) , [DESCRIBE FEATURE POLICY](/sql-reference/sql/desc-feature-policy), [DROP FEATURE POLICY](/sql-reference/sql/drop-feature-policy), [SHOW FEATURE POLICIES](/sql-reference/sql/show-feature-policies)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] FEATURE POLICY [ IF NOT EXISTS ] <name>
  [ BLOCKED_OBJECT_TYPES_FOR_CREATION = ( <type> [ , ... ] ) ]
  [ COMMENT = '<string-literal>' ]
  [ AS $$
      <yaml-body>
    $$ ]
```

## Parameters

`name`
:   Specifies the identifier for the feature policy.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`BLOCKED_OBJECT_TYPES_FOR_CREATION = ( type [ , ... ] )`
:   Specifies a list of objects that can’t be created. The following objects can be blocked:

    - AGENTS
    - APPLICATION\_SERVICE
    - ARTIFACT\_REPOSITORY
    - COMPUTE\_POOLS
    - DATABASES
    - GIT\_REPOSITORY
    - MCP\_SERVERS
    - SCHEMA
    - SECRET
    - TASKS
    - WAREHOUSES
    - WORKSPACE

    Note

    Account-level object types have no effect when a feature policy is bound to personal databases.
    They apply only in a native app context.

    `APPLICATION_SERVICE` and `ARTIFACT_REPOSITORY` are used with
    [Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime).
    Attach a policy that blocks these types to all personal databases to prevent
    users from creating App Runtime apps in their
    [personal databases](/user-guide/personal-databases). For details, see
    [Restrict app creation in personal databases](/developer-guide/snowflake-app-runtime/account-admin-setup#label-snowflake-app-runtime-account-admin-setup-restrict-pdb).

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the feature policy.

    Default: No value

`AS $$ ... $$`
:   Optional YAML body that defines [conditional creation rules](/user-guide/feature-policies#label-feature-policy-rules).
    The body can include `blocked_creation_rules` and an optional `conditions` list.
    For syntax, supported object types, and examples, see
    [Feature policy rules](/user-guide/feature-policies#label-feature-policy-rules).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE FEATURE POLICY | SCHEMA | Grants the ability to create feature policies. You must have this privilege set on the schema containing the policy to be created. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If a policy is bound to an object, for example an account or an app, the policy can’t be replaced.
  Use the [ALTER FEATURE POLICY](/sql-reference/sql/alter-feature-policy) to update or rename the feature policy.
- This command does not support using the CLONE clause to create a copy of a feature policy.
- Specify `BLOCKED_OBJECT_TYPES_FOR_CREATION`, an `AS` body, or both. You can use them together
  in a single policy.

## Examples

The following example creates a new feature policy that prohibits an app from creating a database:

Copy code

```
CREATE FEATURE POLICY block_create_db_policy
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (DATABASES);
```

The following example creates a new feature policy, but doesn’t specify any objects to prohibit.

Copy code

```
CREATE FEATURE POLICY block_nothing_policy
  BLOCKED_OBJECT_TYPES_FOR_CREATION = ();
```

Note

This syntax would typically be applied to an app to lift any restrictions that were applied at
the account level.

The following example creates a feature policy that blocks temporary table creation:

Copy code

```
CREATE FEATURE POLICY block_temp_tables
  AS $$
    blocked_creation_rules:
      - object_type: TABLE
        block_when: "$IS_TEMPORARY"
  $$;
```

A `block_when` expression can read request attributes through the `$` variable shorthand,
as shown, or through the equivalent
`SYS_CONTEXT('SNOWFLAKE$REQUEST', 'GET_OBJECT_PROPERTY', 'IS_TEMPORARY') = 'TRUE'`. For the
available properties and the differences between the two forms, see
[Available context](/user-guide/feature-policies#label-feature-policy-rules-available-context).
