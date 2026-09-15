# ALTER TYPE

Modifies the properties for an existing [user-defined type](/sql-reference/data-types-user-defined).

See also:
:   [CREATE TYPE](/sql-reference/sql/create-type) , [DESCRIBE TYPE](/sql-reference/sql/desc-type) , [SHOW TYPES](/sql-reference/sql/show-types) , [DROP TYPE](/sql-reference/sql/drop-type) , [UNDROP TYPE](/sql-reference/sql/undrop-type)

## Syntax

Copy code

```
ALTER TYPE [ IF EXISTS ] <name> SET
  COMMENT = '<string_literal>'

ALTER TYPE [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the user-defined type to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies the properties to set for the user-defined type:

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the user-defined type.

`UNSET ...`
:   Specifies the properties to unset for the user-defined type, which resets them to the defaults.

    Currently, the only property you can unset is COMMENT, which removes the comment, if one exists, for the user-defined type.

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

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Add a comment to the `age` user-defined type:

Copy code

```
ALTER TYPE age SET COMMENT = 'User-defined type for storing age values';
```

Remove the comment from the `age` user-defined type:

Copy code

```
ALTER TYPE age UNSET COMMENT;
```
