# UNDROP VARIABLE

Restores the most recent version of a dropped [schema variable](/sql-reference/schema-variables).

See also:
:   [CREATE VARIABLE](/sql-reference/sql/create-variable) , [ALTER VARIABLE](/sql-reference/sql/alter-variable) , [DROP VARIABLE](/sql-reference/sql/drop-variable) , [SHOW SCHEMA VARIABLES IN SCHEMA](/sql-reference/sql/show-schema-variables)

## Syntax

Copy code

```
UNDROP VARIABLE <name>
```

## Parameters

`name`
:   Specifies the identifier for the variable to restore. The identifier can be qualified with
    the schema name or with both the database and schema names.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE VARIABLE | Schema |  |
| OWNERSHIP | Variable | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The variable is restored to the schema it was in when it was dropped. If the schema no
  longer exists, the restore fails.
- If a variable with the same name already exists in the schema, an error is returned.
  Drop or rename the existing variable before restoring the older one.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Examples

Restore a dropped variable:

Copy code

```
UNDROP VARIABLE myschema.tax_rate;
```
