# DROP VARIABLE

Removes a [schema variable](/sql-reference/schema-variables) from the schema.

A dropped variable can be recovered within the Time Travel retention period using
[UNDROP VARIABLE](/sql-reference/sql/undrop-variable).

See also:
:   [CREATE VARIABLE](/sql-reference/sql/create-variable) , [ALTER VARIABLE](/sql-reference/sql/alter-variable) , [UNDROP VARIABLE](/sql-reference/sql/undrop-variable) , [SHOW SCHEMA VARIABLES IN SCHEMA](/sql-reference/sql/show-schema-variables)

## Syntax

Copy code

```
DROP VARIABLE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the variable to drop. The identifier can be qualified with
    the schema name or with both the database and schema names.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Variable | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- The `IF EXISTS` modifier suppresses the error if the variable doesn’t exist.
- Dropping a variable doesn’t affect any session variables of the same name.
- A dropped variable can be restored within the [Time Travel](/user-guide/data-time-travel)
  retention period using [UNDROP VARIABLE](/sql-reference/sql/undrop-variable).

## Examples

Drop a variable:

Copy code

```
DROP VARIABLE myschema.tax_rate;
```

Drop a variable only if it exists:

Copy code

```
DROP VARIABLE IF EXISTS myschema.batch_cursor;
```
