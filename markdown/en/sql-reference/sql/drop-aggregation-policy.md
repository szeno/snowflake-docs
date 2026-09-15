# DROP AGGREGATION POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes an [aggregation policy](/user-guide/aggregation-policies) from the current/specified schema.

See also:
:   [Aggregation policy DDL reference](/user-guide/aggregation-policies#label-aggregation-policy-ddl)

## Syntax

Copy code

```
DROP AGGREGATION POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the aggregation policy to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Aggregation policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on aggregation policy DDL and privileges, see [Privileges and commands](/user-guide/aggregation-policies#label-aggregation-policy-manage).

## Usage notes

- Prior to dropping the aggregation policy, execute the following statement to determine if the aggregation policy is set on any tables or
  views.

  Copy code

  ```
  SELECT * FROM TABLE(mydb.INFORMATION_SCHEMA.POLICY_REFERENCES(POLICY_NAME=>'my_agg_policy'));
  ```

  For more information, see [Identify aggregation policy references](/user-guide/aggregation-policies#label-aggregation-constraint-policy-refs).
- An aggregation policy cannot be dropped successfully if it is currently assigned to a table or view.

  Before executing a DROP statement, [detach the aggregation policy](/user-guide/aggregation-policies#label-aggregation-policy-detach) from the table or view with an
  ALTER TABLE or ALTER VIEW statement.

## Example

Drop the aggregation policy:

Copy code

```
DROP AGGREGATION POLICY my_aggpolicy;
```
