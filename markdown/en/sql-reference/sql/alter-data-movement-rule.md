# ALTER DATA MOVEMENT RULE

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Replaces the MAX\_ROWS expression of an existing [data movement rule](/user-guide/data-movement-policies), sets or unsets
its comment, or renames the rule.

Any changes to the rule take effect the next time a data movement policy that uses the rule is evaluated.

See also:
:   [CREATE DATA MOVEMENT RULE](/sql-reference/sql/create-data-movement-rule) , [DROP DATA MOVEMENT RULE](/sql-reference/sql/drop-data-movement-rule) , [SHOW DATA MOVEMENT RULES](/sql-reference/sql/show-data-movement-rules) , [DESCRIBE DATA MOVEMENT RULE](/sql-reference/sql/desc-data-movement-rule)

    [CREATE DATA MOVEMENT POLICY](/sql-reference/sql/create-data-movement-policy) , [ALTER DATA MOVEMENT POLICY](/sql-reference/sql/alter-data-movement-policy) , [DROP DATA MOVEMENT POLICY](/sql-reference/sql/drop-data-movement-policy)

## Syntax

Copy code

```
ALTER DATA MOVEMENT RULE [ IF EXISTS ] <name>
  SET MAX_ROWS AS () RETURNS INTEGER
  -> ( <expression> )

ALTER DATA MOVEMENT RULE [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER DATA MOVEMENT RULE [ IF EXISTS ] <name> UNSET COMMENT

ALTER DATA MOVEMENT RULE [ IF EXISTS ] <name> RENAME TO <new_name>
```

## Parameters

`name`
:   Specifies the identifier for the data movement rule to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the data movement rule; must be unique for your schema. The new identifier can’t be used
    if the identifier is already in place for a different data movement rule.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`SET ...`
:   Specifies one or more properties to set for the data movement rule:

    `MAX_ROWS AS () RETURNS INTEGER -> ( expression )`
    :   SQL expression body that returns an INTEGER, which sets the maximum number of rows that the movement type can move.

        The return value determines the behavior:

        - `NULL` - No limit on the number of rows.
        - `0` - Block the movement.
        - A positive integer - The maximum number of rows that the movement type can move.

        The expression can contain CASE and other logic statements. It can call [SYS\_CONTEXT](/sql-reference/functions/sys_context) to read
        session and movement context and adjust the returned limit accordingly.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the data movement rule.

        Default: No value

`UNSET ...`
:   Specifies the property to unset for the data movement rule, which resets it to its default:

    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Data movement rule | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t change the movement type of an existing data movement rule. To change the movement type, drop the rule and
  create a new one.
- [GET\_DDL](/sql-reference/functions/get_ddl) is supported for this object type. If you want to see the current definition of
  the rule, run the GET\_DDL function.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Lower the row limit on an existing rule:

Copy code

```
ALTER DATA MOVEMENT RULE hr_pii_copy_limit
  SET MAX_ROWS AS () RETURNS INTEGER
  -> (500);
```

Rename a data movement rule:

Copy code

```
ALTER DATA MOVEMENT RULE hr_pii_copy_limit RENAME TO hr_pii_export_limit;
```
