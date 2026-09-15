# DROP SEMANTIC VIEW

Removes the specified [semantic view](/user-guide/views-semantic/overview) from the current/specified schema.

See also:
:   [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) , [ALTER SEMANTIC VIEW](/sql-reference/sql/alter-semantic-view) , [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) , [SHOW SEMANTIC VIEWS](/sql-reference/sql/show-semantic-views) , [SHOW SEMANTIC DIMENSIONS](/sql-reference/sql/show-semantic-dimensions) , [SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) , [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts) , [SHOW SEMANTIC METRICS](/sql-reference/sql/show-semantic-metrics)

## Syntax

Copy code

```
DROP SEMANTIC VIEW [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the semantic view to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Semantic view | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example drops the semantic view named `my_semantic_view`:

Copy code

```
DROP SEMANTIC VIEW my_semantic_view;
```
