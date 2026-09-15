# CREATE TYPE

Creates a [user-defined type](/sql-reference/data-types-user-defined).

See also:
:   [ALTER TYPE](/sql-reference/sql/alter-type) , [DESCRIBE TYPE](/sql-reference/sql/desc-type) , [SHOW TYPES](/sql-reference/sql/show-types) , [DROP TYPE](/sql-reference/sql/drop-type) , [UNDROP TYPE](/sql-reference/sql/undrop-type)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] TYPE [ IF NOT EXISTS ] <name> AS <type>
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the user-defined type; must be unique for the schema in which the user-defined type
    is created.

    The name can’t be the same as a Snowflake type name. For example, the type name can’t be `array` or `geometry`.

    If the name is the same as a [Snowflake keyword](/sql-reference/reserved-keywords), it must be specified
    in double quotes.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`AS type`
:   An existing [Snowflake data type](/sql-reference-data-types) definition.

    The specified type definition is the *base type* for the user-defined type being created.

    `type` can’t be another user-defined type.

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the user-defined type.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE TYPE | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Use the CREATE TYPE command to create a user-defined type based on the NUMBER data type:

Copy code

```
CREATE TYPE age AS NUMBER(3,0);
```

Create a user-defined type based on the OBJECT data type:

Copy code

```
CREATE TYPE path AS OBJECT(
  relative BOOLEAN,
  segments ARRAY(STRING)
);
```

For more examples, see [Examples for user-defined data types](/sql-reference/data-types-user-defined#label-user-defined-type-examples).
