# ALTER VARIABLE

Modifies the properties of an existing [schema variable](/sql-reference/schema-variables).

See also:
:   [CREATE VARIABLE](/sql-reference/sql/create-variable) , [DROP VARIABLE](/sql-reference/sql/drop-variable) , [SHOW SCHEMA VARIABLES IN SCHEMA](/sql-reference/sql/show-schema-variables) , [DESCRIBE VARIABLE](/sql-reference/sql/desc-variable)

## Syntax

Copy code

```
ALTER VARIABLE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER VARIABLE [ IF EXISTS ] <name> SET DEFAULT <default_value>

ALTER VARIABLE [ IF EXISTS ] <name> DROP DEFAULT

ALTER VARIABLE [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER VARIABLE [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the variable to alter. The identifier can be qualified with
    the schema name or with both the database and schema names.

`RENAME TO new_name`
:   Specifies the new identifier for the variable; must be unique within the schema.

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When a variable is renamed, any session variables that shadow it are unaffected because
    session variables and schema variables are resolved by name independently.

`SET DEFAULT default_value`
:   Changes the default value for the variable. The expression is evaluated at statement
    execution time and must be compatible with the variable’s declared data type. To
    reset a variable’s current value to the new default, use `SET schema.name = DEFAULT`.

`DROP DEFAULT`
:   Removes the default value from the variable. The variable’s current value is unchanged;
    only the stored default is cleared.

`SET COMMENT = 'string_literal'`
:   Sets or replaces the comment for the variable.

`UNSET COMMENT`
:   Removes the comment from the variable.

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

- The `IF EXISTS` modifier suppresses the error if the variable doesn’t exist. The statement
  succeeds silently in that case.
- Only metadata properties can be changed with `ALTER VARIABLE`. To change a variable’s
  current value, use [SET](/sql-reference/sql/set) with a qualified name.
- The data type of a variable can’t be changed after creation. Drop and re-create the variable
  to change its type.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename a variable:

Copy code

```
ALTER VARIABLE myschema.tax_rate RENAME TO myschema.regional_tax_rate;
```

Update the default value:

Copy code

```
ALTER VARIABLE myschema.tax_rate SET DEFAULT 0.10;
```

Add a comment:

Copy code

```
ALTER VARIABLE myschema.tax_rate
  SET COMMENT = 'Regional tax rate, updated annually by finance';
```

Remove the default value:

Copy code

```
ALTER VARIABLE myschema.batch_cursor DROP DEFAULT;
```
