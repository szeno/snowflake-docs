# DESCRIBE FEATURE POLICY

Describes the properties of a [feature policy](/user-guide/feature-policies).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE FEATURE POLICY](/sql-reference/sql/create-feature-policy) , [ALTER FEATURE POLICY](/sql-reference/sql/alter-feature-policy), [DROP FEATURE POLICY](/sql-reference/sql/drop-feature-policy), [SHOW FEATURE POLICIES](/sql-reference/sql/show-feature-policies)

## Syntax

Copy code

```
{ DESC | DESCRIBE } FEATURE POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the feature policy to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The command displays properties of a feature policy in the following columns:

| Column | Description |
| --- | --- |
| `property` | The name of the feature property policy. This column can include the properties listed in the following table. |
| `value` | The value assigned to the property of the feature policy. |

Expand

Show lessSee more

The `property` column can include the following properties of a feature policy:

| Property | Description |
| --- | --- |
| `created_on` | The timestamp when the feature policy was created. |
| `name` | The name of the feature policy. |
| `owner` | The role that owns the feature policy. |
| `owner_role_type` | The type of role that owns the object: ROLE or DATABASE\_ROLE |
| `comment` | A description of the feature policy. |
| `blocked_object_types_for_creation` | The list of objects that the feature policy blocks for creation. |
| `policy_definition` | The YAML body for [conditional creation rules](/user-guide/feature-policies#label-feature-policy-rules), if one is set on the policy. Empty when the policy has no body. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY FEATURE POLICY | Account |  |
| OWNERSHIP or APPLY | Feature policy |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example describes the feature policy named `block_db_policy`:

Copy code

```
DESCRIBE FEATURE POLICY block_db_policy;
```

```
+------------------------------------+-------------------------------+
| property                           | value                         |
+------------------------------------|-------------------------------+
| created_on                         | 2025-05-23 08:19:49.483 -0700 |
| name                               | BLOCK_CREATE_DB_POLICY        |
| owner                              | ACCOUNTADMIN                  |
| owner_role_type                    | ROLE                          |
| comment                            |                               |
| blocked_object_types_for_creation  | DATABASES                     |
+------------------------------------+-------------------------------+
```
