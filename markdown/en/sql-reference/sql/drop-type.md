# DROP TYPE

Removes a [user-defined type](/sql-reference/data-types-user-defined).

See also:
:   [CREATE TYPE](/sql-reference/sql/create-type) , [ALTER TYPE](/sql-reference/sql/alter-type) , [DESCRIBE TYPE](/sql-reference/sql/desc-type) , [SHOW TYPES](/sql-reference/sql/show-types) , [UNDROP TYPE](/sql-reference/sql/undrop-type)

## Syntax

Copy code

```
DROP TYPE <name>
```

## Parameters

`name`
:   Specifies the identifier for the user-defined type to drop.

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

- Before you drop a user-defined type, verify that *no* tables or other database objects reference the
  user-defined type.

  You can run SHOW commands to determine which database objects reference a user-defined type. For example,
  the following query runs the [SHOW COLUMNS](/sql-reference/sql/show-columns) command with the
  [pipe operator](/sql-reference/operators-flow) (`->>`) to return tables with columns of data types
  that include the text `AGE`:

  Copy code

  ```
  SHOW COLUMNS ->>
    SELECT "table_name", "data_type"
   FROM $1
   WHERE "data_type" LIKE '%AGE%';
  ```
- If a user-defined type is dropped and a query directly references a column of that type, the query fails.
  Queries that don’t directly reference the column of the dropped type run normally.

## Examples

Use the DROP TYPE command to drop the `age` user-defined type:

Copy code

```
DROP TYPE age;
```
