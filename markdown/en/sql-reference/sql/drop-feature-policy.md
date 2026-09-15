# DROP FEATURE POLICY

Removes the specified feature policy. For an overview, see [Feature policies](/user-guide/feature-policies).

See also:
:   [CREATE FEATURE POLICY](/sql-reference/sql/create-feature-policy) , [ALTER FEATURE POLICY](/sql-reference/sql/alter-feature-policy), [DESCRIBE FEATURE POLICY](/sql-reference/sql/desc-feature-policy), [SHOW FEATURE POLICIES](/sql-reference/sql/show-feature-policies)

## Syntax

Copy code

```
DROP FEATURE POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the feature policy to drop.

If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
Identifiers enclosed in double quotes are also case-sensitive.

For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Feature policy | This privilege is required to drop a feature policy. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage Notes

- A feature policy can’t be dropped if it’s currently applied to an object. First un-apply
  the feature policy using [ALTER ACCOUNT](/sql-reference/sql/alter-account) (for
  account-level bindings) or [ALTER APPLICATION](/sql-reference/sql/alter-application)
  (for app-level bindings), then drop the feature policy.

## Examples

The following example drops the feature policy named `block_db_policy`:

Copy code

```
DROP FEATURE POLICY block_db_policy;
```

```
+---------------------------------------+
| status                                |
|---------------------------------------|
| BLOCK_DB_POLICY successfully dropped. |
+---------------------------------------+
```
