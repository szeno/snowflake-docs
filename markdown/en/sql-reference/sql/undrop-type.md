# UNDROP TYPE

Restores the most recent version of a [user-defined type](/sql-reference/data-types-user-defined).

See also:
:   [CREATE TYPE](/sql-reference/sql/create-type) , [ALTER TYPE](/sql-reference/sql/alter-type) , [DESCRIBE TYPE](/sql-reference/sql/desc-type) , [SHOW TYPES](/sql-reference/sql/show-types) , [DROP TYPE](/sql-reference/sql/drop-type)

## Syntax

Copy code

```
UNDROP TYPE <name>
```

## Parameters

`name`
:   Specifies the identifier for the user-defined type to restore.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | User-defined type | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Restoring user-defined types is only supported in the current schema or current database, even if the type name is fully-qualified.
- If a user-defined type with the same name already exists, an error is returned.

- UNDROP relies on the Snowflake [Time Travel](/user-guide/data-time-travel) feature. An object can be restored only if
  the object was deleted within the [Data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default value is 24 hours.

## Example

Use the UNDROP TYPE command to restore the most recent version of the `age` user-defined type:

Copy code

```
UNDROP TYPE age;
```
