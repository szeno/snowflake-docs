# ALTER FEATURE POLICY

Alters or renames a feature policy. Feature policies can be applied to all databases or a specific database, to all [personal databases](/user-guide/personal-databases#label-personal-databases-feature-policies), or to all [native apps](/developer-guide/native-apps/ui-consumer-feature-policies) or a specific application. For an overview, see [Feature policies](/user-guide/feature-policies).

See also:
:   [CREATE FEATURE POLICY](/sql-reference/sql/create-feature-policy) , [DESCRIBE FEATURE POLICY](/sql-reference/sql/desc-feature-policy), [DROP FEATURE POLICY](/sql-reference/sql/drop-feature-policy), [SHOW FEATURE POLICIES](/sql-reference/sql/show-feature-policies)

## Syntax

Copy code

```
ALTER FEATURE POLICY [ IF EXISTS ] <name> SET
  [ BLOCKED_OBJECT_TYPES_FOR_CREATION = ( [ <type> [ , <type>  ... ] ] ) ]
  [ COMMENT = '<string_literal>' ]
  [ AS $$
      <yaml-body>
    $$ ]

ALTER FEATURE POLICY [ IF EXISTS ] <name>
  AS $$
      <yaml-body>
    $$

ALTER FEATURE POLICY [ IF EXISTS ] <name> UNSET
  [ BLOCKED_OBJECT_TYPES_FOR_CREATION ]
  [ COMMENT ]
  [ POLICY_DEFINITION ]

ALTER FEATURE POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER FEATURE POLICY [ IF EXISTS ] <name> SET  TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER FEATURE POLICY [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , ... ]
```

## Parameters

`name`
:   Specifies the identifier for the feature policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET`
:   Specifies one (or more) properties to set for the feature policy.

    `BLOCKED_OBJECT_TYPES_FOR_CREATION = ( type [ , type ... ] )`
    :   Specifies the objects that are prohibited from being created.

        Possible values are:

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

    `COMMENT = 'string_literal'`
    :   String (literal) that specifies a comment for the feature policy.

`AS $$ ... $$`
:   YAML body that defines [conditional creation rules](/user-guide/feature-policies#label-feature-policy-rules).
    Replaces any existing policy body. You can use this clause with `SET` or as a
    standalone clause. For syntax and examples, see
    [Feature policy rules](/user-guide/feature-policies#label-feature-policy-rules) and
    [Modify or remove a policy body](/user-guide/feature-policies#label-feature-policy-rules-modify).

`UNSET`
:   Specifies one (or more) properties to unset for the feature policy.

    `BLOCKED_OBJECT_TYPES_FOR_CREATION`
    :   Removes the list of blocked object types from the feature policy.

    `COMMENT`
    :   Removes the comment for the feature policy.

    `POLICY_DEFINITION`
    :   Removes the YAML policy body but keeps any `BLOCKED_OBJECT_TYPES_FOR_CREATION` clause.

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY FEATURE POLICY | Account | This privilege is required to set a feature policy for the current account. |
| APPLY or OWNERSHIP | Feature policy | One of these privileges is required to modify a feature policy. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If a previous policy had been applied to the account or an object, an error is returned unless you
  specify the FORCE option to force the replacement of the existing policy.
- When a feature policy is unbound from an app, the account-level `FOR ALL APPLICATIONS` policy
  takes effect for that app, if one exists.
- When a feature policy is unbound from a database, the account-level `FOR ALL DATABASES` (or
  `FOR ALL PERSONAL DATABASES` for personal databases) policy takes effect, if one exists.

## Examples

The following example sets the BLOCKED\_OBJECT\_TYPES\_FOR\_CREATION property on the feature policy
to prohibit an app from creating databases or tasks:

Copy code

```
ALTER FEATURE POLICY block_create_db_policy SET
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (DATABASES, TASKS);
```

The following example replaces the YAML body of a feature policy:

Copy code

```
ALTER FEATURE POLICY my_policy AS $$
  blocked_creation_rules:
    - object_type: TABLE
      block_when: "$IS_TEMPORARY"
$$;
```

The `block_when` expression uses the `$` variable shorthand. For the available properties
and the equivalent `SYS_CONTEXT` form, see
[Available context](/user-guide/feature-policies#label-feature-policy-rules-available-context).

The following example removes the YAML body but keeps any blocked object types:

Copy code

```
ALTER FEATURE POLICY my_policy UNSET POLICY_DEFINITION;
```

The following example changes the name of a feature policy from `block_create_db_policy` to
`block_create_db_task_policy`:

Copy code

```
ALTER FEATURE POLICY block_create_db_policy RENAME TO block_create_db_task_policy;
```
