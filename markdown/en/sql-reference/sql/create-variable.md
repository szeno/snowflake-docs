# CREATE VARIABLE

Creates a new [schema variable](/sql-reference/schema-variables), a named, typed, persistent scalar value scoped to a schema.

See also:
:   [ALTER VARIABLE](/sql-reference/sql/alter-variable) , [DROP VARIABLE](/sql-reference/sql/drop-variable) , [UNDROP VARIABLE](/sql-reference/sql/undrop-variable) , [SHOW SCHEMA VARIABLES IN SCHEMA](/sql-reference/sql/show-schema-variables) , [DESCRIBE VARIABLE](/sql-reference/sql/desc-variable)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] VARIABLE [ IF NOT EXISTS ] <name> <data_type>
  [ DEFAULT <default_value> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the variable. The identifier must be unique within the schema.

    The identifier can be optionally qualified with the schema name (`schema.variable_name`) or
    with both the database and schema names (`database.schema.variable_name`).

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`data_type`
:   Specifies the data type of the variable. All scalar Snowflake data types are supported.
    The value stored in the variable must be assignment-compatible with this type.

    For the list of supported types, see [Summary of data types](/sql-reference/intro-summary-data-types).

## Optional parameters

`DEFAULT default_value`
:   Specifies the initial value for the variable. The expression is evaluated at creation time
    and must produce a value compatible with `data_type`. If omitted, the variable’s initial
    value is NULL.

    The default can be changed after creation with [ALTER VARIABLE … SET DEFAULT](/sql-reference/sql/alter-variable).

`COMMENT = 'string_literal'`
:   Specifies a comment for the variable.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE VARIABLE | Schema |  |
| OWNERSHIP | Variable | Required to execute a CREATE OR REPLACE VARIABLE statement for an *existing* variable.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege).  Note that in a [managed access schema](/user-guide/security-access-control-configure#label-managed-access-schemas), only the schema owner (i.e. the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege can grant or revoke privileges on objects in the schema, including future grants. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Creating a variable automatically grants `OWNERSHIP` on that variable to the role that created it.
- The maximum size of a variable’s value is 256 bytes.
- Unquoted variable names are case-insensitive. For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create a variable to hold a tax rate, with a default value:

Copy code

```
CREATE VARIABLE myschema.tax_rate FLOAT DEFAULT 0.08;
```

Create a variable with a comment:

Copy code

```
CREATE VARIABLE myschema.api_version VARCHAR
  DEFAULT 'v2'
  COMMENT = 'REST API version used by all stored procedures in this schema';
```

Create a variable using the fully qualified name:

Copy code

```
CREATE VARIABLE mydb.myschema.environment VARCHAR DEFAULT 'production';
```

Create a variable only if it doesn’t already exist:

Copy code

```
CREATE VARIABLE IF NOT EXISTS myschema.batch_cursor NUMBER DEFAULT 0;
```
